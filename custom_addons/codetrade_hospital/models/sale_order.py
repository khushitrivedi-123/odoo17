from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    treatment_id = fields.Many2one(
        "hospital.treatment",
        string="Treatment",
        help="Related Treatment for this Sale Order",
    )
    treatment_code = fields.Char(
        string="Treatment Code",
        related="treatment_id.treatment_code",
        store=True,
        readonly=True,
    )

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'treatment_id': self.treatment_id.id,
        })
        return invoice_vals