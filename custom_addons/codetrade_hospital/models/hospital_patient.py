from odoo import models, fields, api
from datetime import date
import re
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherits = {'res.users': 'user_id'}
    _description = 'Hospital Patient'

    patient_name = fields.Char(string="Patient Name", required=True)

    age = fields.Integer(string="Age", compute='_compute_age', store=True)

    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender", required=True)

    contact_number = fields.Char(string="Contact Number", required=True)

    email = fields.Char(string="Email", required=True)

    date_of_birth = fields.Date(string="Date of Birth", required=True)

    physician_id = fields.Many2one('hospital.physician', string="Assigned Physician")

    user_id = fields.Many2one('res.users', string="Related User", ondelete="cascade")

    @api.constrains('email')
    def _check_email_format(self):
        for patient in self:
            if patient.email:
                email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                if not re.match(email_regex, patient.email):
                    raise ValidationError("The email address is not in a valid format.")

    @api.depends('date_of_birth')
    def _compute_age(self):
        for patient in self:
            if patient.date_of_birth:
                today = date.today()
                birthdate = fields.Date.from_string(patient.date_of_birth)
                if birthdate > today:
                    raise ValidationError("Date of birth cannot be in the future.")
                age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
                patient.age = age
            else:
                patient.age = 0

    @api.model
    def create(self, vals):
        # import pdb;pdb.set_trace()
        vals['name'] = vals.get('patient_name')
        vals['login'] = vals.get('email')
        return super(HospitalPatient, self).create(vals)
