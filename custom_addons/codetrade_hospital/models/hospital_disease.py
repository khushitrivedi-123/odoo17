from odoo import models, fields

class HospitalDisease(models.Model):
    _name = 'hospital.disease'
    _description = 'Disease'

    name = fields.Char(string="Disease Name", required=True)
    code = fields.Char(string="Code", required=True)

