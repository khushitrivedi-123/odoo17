import logging
from odoo import http
from odoo.http import request

class PatientFormController(http.Controller):

    @http.route('/patient_webform', type='http', auth="public", website=True)
    def patient_webform(self, **kwargs):
        # import pdb;pdb.set_trace()
        return http.request.render('codetrade_hospital_website.create_patient',{})

    @http.route('/submit_patient/', type='http', auth="public",  website=True, csrf=False)
    def submit_patient_form(self, **kwargs):
        # import pdb; pdb.set_trace()
        _logger = logging.getLogger(__name__)
        _logger.info("Submit patient form was triggered.")

        request.env['hospital.patient'].sudo().create({
            'patient_name': kwargs.get('patient_name'),
            'date_of_birth': kwargs.get('date_of_birth'),
            'age': kwargs.get('age'),
            'gender': kwargs.get('gender'),
            'contact_number': kwargs.get('contact_number'),
            'email': kwargs.get('email_from'),
        })

        return request.render("codetrade_hospital_website.website_patient_thank_you", {})
