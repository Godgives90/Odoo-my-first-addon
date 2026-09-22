from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Descrizione del secondo modello del modulo di Antonio D."
    _order = "sequence, name"



    name = fields.Char('Nome', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Proprietà')
    sequence = fields.Integer('Sequenza')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(string='Numero di offerte', compute='_compute_offer_count')


#controllo dati inseriti nei campi
    _sql_constraints = [
        ('type_name_uniq', 'unique (name)', "Tipo di proprietà già esistente"),
    ]

# computazione campi
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
