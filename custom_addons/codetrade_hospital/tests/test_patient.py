from odoo.tests import common
from odoo.exceptions import ValidationError
from odoo import fields

class TestHospitalPatient(common.TransactionCase):

    def test_invalid_email_validation(self):
        with self.assertRaises(ValidationError):
            self.env['hospital.patient'].create({
                'patient_name': 'demo',
                'gender': 'male',
                'contact_number': '7894561230',
                'email': 'invalid-email',
                'date_of_birth': '2003-01-01',
            })

    def test_email_validation(self):
        valid_email = "test1@example.com"
        # import pdb;pdb.set_trace()
        patient = self.env['hospital.patient'].create({
            'patient_name': 'demo',
            'gender': 'male',
            'contact_number': '7894561230',
            'email': valid_email,
            'date_of_birth': '2003-01-01',
        })
        self.assertEqual(patient.email, valid_email, "Valid email should be accepted.")

    def test_future_date_of_birth(self):
        with self.assertRaises(ValidationError):
            self.env['hospital.patient'].create({
                'patient_name': 'demo',
                'gender': 'male',
                'contact_number': '9876543210',
                'email': 'abc@gmail.com',
                'date_of_birth': '3000-01-01',
            })

    def test_date_of_birth(self):
        # import pdb;pdb.set_trace()
        patient = self.env['hospital.patient'].create({
            'patient_name': 'demo',
            'gender': 'male',
            'contact_number': '9876543210',
            'email': 'abc@gmail.com',
            'date_of_birth': '2003-01-01',
        })
        expected_date_of_birth = fields.Date.from_string('2003-01-01')
        self.assertEqual(patient.date_of_birth, expected_date_of_birth)
