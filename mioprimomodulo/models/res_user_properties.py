from odoo import api, fields, models

class EstateProperty(models.Model):
    _inherit = "res.users"
    _description = "Descrizione della prima inheritance del modulo di Antonio D."

    property_ids = fields.One2many('estate.property', 'salesperson_id', domain=["|", ("state", "=", "new"), ("state", "=", "offer received")])
