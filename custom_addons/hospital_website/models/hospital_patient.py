from odoo import models

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = 'res.partner'

    def _create_res_partner(self, vals):
        # Prevent creation of partner automatically
        return False
