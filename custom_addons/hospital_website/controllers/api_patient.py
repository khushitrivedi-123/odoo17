from odoo import http
from odoo.http import request
import json


class HospitalPatientAPI(http.Controller):

    @http.route('/api/patient/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_patient(self):
        try:
            post = request.httprequest.get_json()

            required_fields = ["patient_name", "email", "contact_number", "date_of_birth", "gender"]

            missing_fields = [field for field in required_fields if field not in post]
            if missing_fields:
                return {"status": "error", "message": f"Missing fields: {', '.join(missing_fields)}"}

            patient = request.env["hospital.patient"].sudo().create({
                "patient_name": post.get("patient_name"),
                "email": post.get("email"),
                "contact_number": post.get("contact_number"),
                "date_of_birth": post.get("date_of_birth"),
                "gender": post.get("gender"),
                "company_id": request.env.company.id,
            })

            return {
                "status": "success",
                "message": "Patient created successfully",
                "patient_id": patient.id,
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}
