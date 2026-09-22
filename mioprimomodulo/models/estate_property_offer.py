from odoo import fields, models, api
from odoo.tools.convert import relativedelta
from odoo.tools import float_utils
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Descrizione del quarto modello del modulo di Antonio Donadio"
    _order = "price desc"



    price = fields.Float('Offerta')
    status = fields.Selection(
        string='Stato',
        selection=[('accepted', 'Accettata'), ('refused', 'Rifiutata')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string='Offerente', required=True)
    property_id = fields.Many2one('estate.property', 'offer_ids', required=True)
    validity = fields.Integer('Validità', default=7)
    date_deadline = fields.Date('Scadenza', compute='_compute_deadline', inverse='_inverse_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)





    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            bestPrice = self.env['estate.property'].browse(val['property_id']).best_price            
            if float_utils.float_compare(bestPrice, val['price'], 2) != -1:
                raise ValidationError(f'L\'offerta deve essere più alta di ' + str(format(bestPrice, '.2f')).replace('.', ','))
            self.env['estate.property'].browse(val['property_id']).offer_received_on_creation()
        return super(EstatePropertyOffer, self).create(vals)

#controllo dati inseriti nei campi
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'Il valore di un\'offerta di un immobile deve essere rigorosamente positivo')
    ]

# computazione campi
    @api.depends('create_date', 'validity', 'date_deadline')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.date.today() + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days



#azioni dei bottoni
    def action_accepted(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == 'accepted' or offer.status == False:
                    offer.status = 'refused'
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer accepted'
        return True

    def action_refused(self):
        for record in self:
            record.status = 'refused'
        return True


#|----------------------| Bottone test |----------------------|
    
    def action_offer_test(self):
        for record in self:
            print('|-----------| inizio |------------|')
            print(len(self.property_id.offer_ids) == 0)
            print('|-----------|  fine  |------------|')
        return True
