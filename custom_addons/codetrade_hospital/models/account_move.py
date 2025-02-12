from odoo import models, fields, api, _
import logging
from odoo.tools import formatLang
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    treatment_id = fields.Many2one(
        "hospital.treatment",
        string="Treatment",
        help="Select the related treatment for this invoice.",
    )

    treatment_code = fields.Char(related="treatment_id.treatment_code", string="Treatment Code", readonly=True)

    @api.depends('move_type', 'line_ids.amount_residual')
    def _compute_payments_widget_reconciled_info(self):
        for move in self:
            payments_widget_vals = {'title': _('Less Payment'), 'outstanding': False, 'content': []}

            if move.state == 'posted' and move.is_invoice(include_receipts=True):
                reconciled_vals = []
                reconciled_partials = move.sudo()._get_all_reconciled_invoice_partials()
                for reconciled_partial in reconciled_partials:
                    counterpart_line = reconciled_partial['aml']

                    # Handling reference display
                    reconciliation_ref = '%s (%s)' % (counterpart_line.move_id.name, counterpart_line.move_id.ref) if counterpart_line.move_id.ref else counterpart_line.move_id.name

                    # Foreign currency handling
                    foreign_currency = counterpart_line.currency_id if counterpart_line.amount_currency and counterpart_line.currency_id != counterpart_line.company_id.currency_id else False

                    # Fetch treatment details safely
                    treatment_id = counterpart_line.move_id.treatment_id.id if counterpart_line.move_id.treatment_id else False
                    treatment_code = counterpart_line.move_id.treatment_id.treatment_code if counterpart_line.move_id.treatment_id else "N/A"

                    # Log the treatment values to check correctness
                    _logger.info(f"Processing move {move.name} - Treatment ID: {treatment_id}, Treatment Code: {treatment_code}")

                    reconciled_vals.append({
                        'name': counterpart_line.name,
                        'journal_name': counterpart_line.journal_id.name,
                        'company_name': counterpart_line.journal_id.company_id.name if counterpart_line.journal_id.company_id != move.company_id else False,
                        'amount': reconciled_partial['amount'],
                        'currency_id': move.company_id.currency_id.id if reconciled_partial['is_exchange'] else reconciled_partial['currency'].id,
                        'date': counterpart_line.date,
                        'partial_id': reconciled_partial['partial_id'],
                        'account_payment_id': counterpart_line.payment_id.id,
                        'payment_method_name': counterpart_line.payment_id.payment_method_line_id.name,
                        'move_id': counterpart_line.move_id.id,
                        'ref': reconciliation_ref,
                        'is_exchange': reconciled_partial['is_exchange'],
                        'amount_company_currency': formatLang(self.env, abs(counterpart_line.balance), currency_obj=counterpart_line.company_id.currency_id),
                        'amount_foreign_currency': foreign_currency and formatLang(self.env, abs(counterpart_line.amount_currency), currency_obj=foreign_currency),
                        'treatment_id': treatment_id if treatment_id else None,  # Ensure None instead of False
                        'treatment_code': treatment_code if treatment_code != "N/A" else None,  # Ensure None when not available
                    })

                payments_widget_vals['content'] = reconciled_vals

            move.invoice_payments_widget = payments_widget_vals if payments_widget_vals['content'] else False