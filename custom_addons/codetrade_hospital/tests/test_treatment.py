from odoo.tests import TransactionCase


class TestHospitalTreatment(TransactionCase):
    def setUp(self):
        super(TestHospitalTreatment, self).setUp()

        self.patient = self.env['hospital.patient'].create({
            'patient_name': 'Test Patient',
            'email': 'testpatient@example.com',
            'gender': 'male',
            'contact_number': '7894561230',
            'date_of_birth': '2003-01-01',
        })

        self.physician = self.env['hospital.physician'].create({
            'physician_name': 'Test Physician',
            'email': 'testphysician@gmail.com',
        })

        self.treatment = self.env['hospital.treatment'].create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'treatment_date': '2025-01-29'
        })

    def test_set_active(self):
        self.assertEqual(self.treatment.state, 'draft')
        self.treatment.set_active()
        self.assertEqual(self.treatment.state, 'active')

    def test_set_done(self):
        self.treatment.set_active()
        self.assertEqual(self.treatment.state, 'active')
        self.treatment.set_done()
        self.assertEqual(self.treatment.state, 'done')
