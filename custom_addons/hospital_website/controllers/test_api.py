from odoo import http
from odoo.http import request


class HospitalPatientAPI(http.Controller):

    @http.route('/api/patient/search', type='json', auth='public', methods=['POST'], csrf=False)
    def search_patient(self):
        try:
            post = request.httprequest.get_json()

            search_domain = []
            if "patient_name" in post:
                search_domain.append(("patient_name", "ilike", post.get("patient_name")))
            if "email" in post:
                search_domain.append(("email", "=", post.get("email")))
            if "contact_number" in post:
                search_domain.append(("contact_number", "=", post.get("contact_number")))

            if not search_domain:
                return {"status": "error", "message": "Please provide at least one search parameter (patient_name, email, or contact_number)."}

            patients = request.env["hospital.patient"].sudo().search(search_domain)

            if not patients:
                return {"status": "error", "message": "No patient found with the given details."}

            patient_list = []
            for patient in patients:
                patient_list.append({
                    "patient_id": patient.id,
                    "patient_name": patient.patient_name,
                    "email": patient.email,
                    "contact_number": patient.contact_number,
                    "date_of_birth": str(patient.date_of_birth),
                    "gender": patient.gender
                })

            return {
                "status": "success",
                "message": "Patient(s) found successfully",
                "patients": patient_list
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}





# class TestApi(http.Controller):
#     @http.route("/api/test", methods=["GET"], type="http", auth="none", csrf=False)
#     def test_endpoint(self):
#         response_data = {
#             "status": "success",
#             "message": "Patient created successfully",
#         }
#         return Response(json.dumps(response_data), content_type="application/json", status=200)