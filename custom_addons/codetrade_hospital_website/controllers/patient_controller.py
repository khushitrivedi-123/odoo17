from odoo import http
from odoo.http import request

class PatientFormController(http.Controller):

    @http.route('/submit_patient', type='http', auth="public", website=True)
    def submit_patient_form(self, **post):
        _logger = logging.getLogger(__name__)
        _logger.info("Submit patient form was triggered.")
        # Creating a new patient record using the submitted form data
        request.env['hospital.patient'].sudo().create({
            'name': post.get('patient_name'),
            'date_of_birth': post.get('date_of_birth'),
            'age': post.get('age'),
            'gender': post.get('gender'),
            'contact_number': post.get('contact_number'),
            'email': post.get('email_from'),
        })
        # Redirect to the thank you page
        return request.redirect('/patient-thank-you')
