from odoo import http
from odoo.http import request


class HospitalFormController(http.Controller):

    @http.route("/my/form", type="http", auth="public", website=True)
    def render_form(self):
        return request.render("hospital_website.form_template")

    @http.route("/my/form/submit", type="http", auth="public", website=True, csrf=True)
    def submit_form(self, **post):
        request.env["hospital.patient"].sudo().create(
            {
                "patient_name": post.get("patient_name"),
                "email": post.get("email"),
                "gender": post.get("gender"),
                "contact_number": post.get("contact_number"),
                "date_of_birth": post.get("date_of_birth"),
            }
        )

        return request.redirect("/thank-you")

    @http.route("/thank-you", type="http", auth="public", website=True)
    def thank_you_page(self):
        return request.render("hospital_website.thank_you_template")

    @http.route("/register-patient", type="http", auth="public", website=True)
    def register_patient(self):
        return request.render("hospital_website.form_template")
