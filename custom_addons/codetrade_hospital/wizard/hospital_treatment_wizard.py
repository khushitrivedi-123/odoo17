from odoo import models, fields, api

class HospitalTreatmentWizard(models.TransientModel):
    _name = 'hospital.treatment.wizard'
    _description = 'Sales Description for Patient'

    treatment_id = fields.Many2one('hospital.treatment', string="Treatment", required=True, default=lambda self: self.env.context.get('default_treatment_id'))

    product_ids = fields.Many2many('product.product', string='Products', required=True)

    def confirm_action(self):
        if not self.treatment_id:
            raise UserError("The treatment_id is not set!")

        sale_order = self.create_sale_order()
        return {
            'type': 'ir.actions.act_window_close',
            'res_id': sale_order.id,
            'res_model': 'sale.order',
            'view_mode': 'form',
            'target': 'current',
        }

    def create_sale_order(self):
        if not self.product_ids:
            raise UserError("Please select at least one product to create a sale order.")

        partner_id = self.treatment_id.patient_id.partner_id.id
        if not partner_id:
            raise UserError("The patient does not have an associated partner.")

        order_lines = [(0, 0, {'product_id': product.id, 'product_uom_qty': 1}) for product in self.product_ids]

        sale_order = self.env['sale.order'].create({
            'partner_id': partner_id,
            'treatment_id': self.treatment_id.id,
            'order_line': order_lines,
        })

        return sale_order
