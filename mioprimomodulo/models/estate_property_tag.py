from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Descrizione del terzo modello del modulo di Antonio D."
    _order = "name"



    name = fields.Char('Nome', required=True)
    color = fields.Integer('Colore')



    #controllo dati inseriti nei campi
    _sql_constraints = [
        ('tags_name_uniq', 'unique (name)', "Tag già esistente"),
    ]
