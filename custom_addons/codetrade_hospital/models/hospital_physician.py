from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError

class HospitalPhysician(models.Model):
    _name = 'hospital.physician'
    _description = 'Hospital Physician'

    name = fields.Char(string="Physician Name", required=True)

    specialization = fields.Char(string="Specialization")

    contact_number = fields.Char(string="Contact Number")

    email = fields.Char(string="Email", required=True)

    hospital_id = fields.Many2one('res.partner', string="Hospital")

    specialization_ids = fields.Many2many('hospital.specialty', string="Specialties")

    @api.constrains('email')
    def _check_email_format(self):
        for physician in self:
            if physician.email:
                email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                if not re.match(email_regex, physician.email):
                    raise ValidationError("The email address is not in a valid format.")
