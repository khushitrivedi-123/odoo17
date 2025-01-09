from odoo import models, fields

class HospitalSpecialty(models.Model):
    _name = 'hospital.specialty'
    _description = 'Physician Specialty'

    name = fields.Char(string="Specialty Name", required=True)
    code = fields.Char(string="Specialty Code", required=True, unique=True)
