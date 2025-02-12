from odoo import http
from odoo.http import request
import json

class PatientApi(http.Controller):

    @http.route('/create/api/patient', type='json', auth='none', methods=["POST"], csrf=False)
    def post_patient(self, **kwargs):
        try:
            byte_data = request.httprequest.data
            decoded_data = byte_data.decode('utf-8')
            vals = json.loads(decoded_data)

            print("Received API Data:", vals)

            if not vals.get("patient_name"):
                return {"error": "patient_name is required"}
            # company_id = vals.get("company_id")
            # company = request.env["res.company"].sudo().search([('name','=',company_id)])
            import pdb;pdb.set_trace()
            patient = request.env["hospital.patient"].sudo().create({
                "patient_name": vals.get("patient_name"),
                "email": vals.get("email"),
                "gender": vals.get("gender"),
                "contact_number": vals.get("contact_number"),
                "date_of_birth": vals.get("date_of_birth"),
                # "res_company_id": company.id,
                "res_company_id": 1,
            })

            return request.make_json_response({
                "message": "Patient has been created successfully",
                "patient_id": patient.id
            }, status=200)

        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)
