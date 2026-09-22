from odoo import api, fields, models, exceptions
from odoo.tools.convert import relativedelta
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Descrizione del primo modello del modulo di Antonio D."
    _order = "id desc"

    
# Campi vista principale
    title = fields.Char('Titolo', required=True)
    description = fields.Text('Descrizione')
    postcode = fields.Char('Codice postale')
    date_availability = fields.Date(
        string='Data disponibilità', 
        default=(fields.Date.today() + relativedelta(months=3)), 
        copy=False)
    expected_price = fields.Float('Prezzo previsto', required=True)
    selling_price = fields.Float('Prezzo di vendita', copy=False, readonly=True)
    bedrooms = fields.Integer('Camere da letto', default=2)
    living_area = fields.Integer('Area salotto (mq)')
    facades = fields.Integer('Facciate')
    garage = fields.Boolean()
    garden = fields.Boolean('Giardino')
    garden_area = fields.Integer('Area giardino (mq)')
    garden_orientation = fields.Selection(
        string='Orientamento giardino',
        selection=[('north', 'Nord'), ('south', 'Sud'), ('east', 'Est'), ('west', 'Ovest')],
    )
    active = fields.Boolean('Attivo', default=True)
    state = fields.Selection(
        string='Stato',
        selection=[('new', 'Nuovo'), ('offer received', 'Offerta ricevuta'), ('offer accepted', 'Offerta accettata'), ('sold', 'Venduto'), ('canceled', 'Annullato')],
        default='new',
        copy=False,
        required=True,
    )
    property_type_id = fields.Many2one('estate.property.type', string='Tipo di proprietà')
    salesperson_id = fields.Many2one('res.users', string='Venditore', default=lambda self: self.env.user) # index=True, tracking=True,
    buyer_id = fields.Many2one('res.partner', string='Acquirente')
    tag_ids = fields.Many2many('estate.property.tag', string='Etichette')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offerte')
    total_area = fields.Integer('Area totale (mq)', compute='_compute_total_area')
    best_price = fields.Float('Offerta migliore', compute='_compute_best_price', store=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, required=True)    

    @api.ondelete(at_uninstall=False)
    def _unlink_if_house_new_or_canceled(self):
        if self.state != 'new' and self.state != 'canceled':
            raise exceptions.UserError("Non è possibile eliminare immobili se lo stato non è nuovo o annullato ")
    
    def offer_received_on_creation(self):
        self.state = 'offer received'

#controllo dati inseriti nei campi
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'Il prezzo previsto di un immobile deve essere rigorosamente positivo'),

        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'Il prezzo di vendita di un immobile deve essere positivo')
    ]

    @api.constrains('expected_price', 'selling_price')
    def check_selling_price(self):
        for record in self:
            minPrice = ((record.expected_price * 90) /100)
            if float_utils.float_compare(minPrice, record.selling_price, 2) == 1 and not float_utils.float_is_zero(record.selling_price, 2):
               raise exceptions.ValidationError('Il prezzo di vendita deve essere almeno il 90' + '%' +  ' del prezzo previsto!')
    

    
# computazione campi    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids) > 0:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.00

    @api.onchange('garden')
    def onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.onchange('offer_ids')
    def _new_if_empty_offers(self):
        if len(self.offer_ids) == 0:
            self.state = 'new'

   
#azioni dei bottoni
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError('Proprietà annullate non possono essere vendute')
            else:
                record.state = 'sold'
        return True

    def action_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError('Proprietà vendute non possono essere annullate')
            else:
                record.state = 'canceled'
        return True


#|----------------------| Bottone test |----------------------|
    
    def action_test(self):
        for record in self:
            print('|-----------| inizio |------------|')
            print(record.offer_ids.mapped('price'))
            print(self)
            print('|-----------|  fine  |------------|')
        return True
