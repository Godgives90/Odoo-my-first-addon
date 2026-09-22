from odoo import api, fields, models, exceptions

class EstateProperty(models.Model):
    _inherit = "estate.property"


    def action_sold(self):
        print('action sold dal modello estate_account')
        return super(EstateProperty, self).action_sold()