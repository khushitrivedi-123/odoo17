from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HospitalTreatment(models.Model):
    _name = 'hospital.treatment'
    _description = 'Treatment'
    _rec_name = 'treatment_code'

    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True, help="The patient receiving the treatment")
    physician_id = fields.Many2one('hospital.physician', string="Physician", required=True, help="The physician providing the treatment")
    treatment_date = fields.Date(string="Treatment Date", required=True, default=fields.Date.today, help="The date of the treatment")
    diagnosis_line_id = fields.One2many('hospital.diagnosis', 'treatment_id', string="Treatments")
    sale_order_ids = fields.One2many('sale.order', 'treatment_id', string='Sales Orders')
    sale_order_count = fields.Integer(string="Sales Orders Count", compute='_compute_sale_order_count', store=True)
    treatment_code = fields.Char(string="Treatment Code", readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('hospital.treatment'))
    image = fields.Binary(string="Treatment Image", attachment=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('done', 'Done')
    ], default='draft', string="State")

    def set_active(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'active'
    def set_done(self):
        for record in self:
            if record.state == 'active':
                record.state = 'done'

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        for record in self:
            record.sale_order_count = self.env['sale.order'].search_count(
                [('treatment_id', '=', record.id)]
            )

    def action_open_sale_orders(self):
        return {
            'name': 'Sales Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('treatment_id', '=', self.id)],
            'context': {'default_treatment_id': self.id},
        }

    def action_download_blank_report(self):
        return self.env.ref('codetrade_hospital.hospital_treatment_report_action').report_action(self)

    @api.constrains('diagnosis_line_id')
    def _check_high_diagnosis(self):
        for record in self:
            high_count = sum(1 for line in record.diagnosis_line_id if line.diagnosis_type == 'high')
            if high_count > 1:
                raise ValidationError("The diagnosis type 'high' can only be selected once per treatment.")

