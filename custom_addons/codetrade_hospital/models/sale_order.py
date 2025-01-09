from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    treatment_id = fields.Many2one('hospital.treatment', string='Treatment', help="Related Treatment for this Sale Order")
    treatment_code = fields.Char(string="Treatment Code", related='treatment_id.treatment_code', store=True, readonly=True)

