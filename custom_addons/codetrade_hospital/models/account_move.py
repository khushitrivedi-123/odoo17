from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    treatment_id = fields.Many2one(
        "hospital.treatment",
        string="Treatment",
        help="Select the related treatment for this invoice.",
    )

    # treatment_code = fields.Char(related="treatment_id.treatment_code", string="Treatment Code", readonly=True,)
