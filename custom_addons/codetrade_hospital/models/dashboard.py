from odoo import models, fields, api

class HospitalDashboard(models.Model):
    _name = "hospital.dashboard"
    _description = "Hospital Dashboard"

    patient_count = fields.Integer(string="Patients", compute="_compute_patient_count")
    physician_count = fields.Integer(string="Physicians", compute="_compute_physician_count")
    treatment_count = fields.Integer(string="Treatments", compute="_compute_treatment_count")

    name = fields.Char(string="Name")

    @api.depends()
    def _compute_patient_count(self):
        for record in self:
            record.patient_count = self.env['hospital.patient'].search_count([])

    @api.depends()
    def _compute_physician_count(self):
        for record in self:
            record.physician_count = self.env['hospital.physician'].search_count([])

    @api.depends()
    def _compute_treatment_count(self):
        for record in self:
            record.treatment_count = self.env['hospital.treatment'].search_count([])

    def action_open_patients(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Patients',
            'res_model': 'hospital.patient',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def action_open_physicians(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Physicians',
            'res_model': 'hospital.physician',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def action_open_treatments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Treatments',
            'res_model': 'hospital.treatment',
            'view_mode': 'tree,form',
            'target': 'current',
        }
