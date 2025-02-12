from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HospitalTreatment(models.Model):
    _name = "hospital.treatment"
    _description = "Treatment"
    _rec_name = "treatment_code"

    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True, help="The patient receiving the treatment")
    physician_id = fields.Many2one("hospital.physician", string="Physician", required=True, help="The physician providing the treatment")
    treatment_date = fields.Date(string="Treatment Date", required=True, default=fields.Date.today, help="The date of the treatment")
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company, required=True)
    diagnosis_line_id = fields.One2many("hospital.diagnosis", "treatment_id", string="Treatments")
    sale_order_ids = fields.One2many("sale.order", "treatment_id", string="Sales Orders")
    sale_order_count = fields.Integer(string="Sales Orders Count", compute="_compute_sale_order_count", store=True)
    treatment_code = fields.Char(string="Treatment Code", readonly=True, default=lambda self: self.env["ir.sequence"].next_by_code("hospital.treatment"))
    image = fields.Binary(string="Treatment Image", attachment=True)
    state = fields.Selection(
        [("draft", "Draft"), ("active", "Active"), ("done", "Done")],
        default="draft",
        string="State",
    )
    has_high_diagnosis_past = fields.Boolean(
        string="Has High Diagnosis (Past & Today)",
        compute="_compute_has_high_diagnosis_past",
        store=True,
    )

    def set_active(self):
        for record in self:
            if record.state == "draft":
                record.state = "active"

    def set_done(self):
        for record in self:
            if record.state == "active":
                record.state = "done"
                if record.patient_id.email:
                    template = self.env.ref(
                        "codetrade_hospital.email_template_treatment_done"
                    )
                    if template:
                        template.send_mail(record.id, force_send=True)
                else:
                    raise ValidationError("The patient does not have an email address.")


    @api.depends("sale_order_ids")
    def _compute_sale_order_count(self):
        for record in self:
            record.sale_order_count = self.env["sale.order"].search_count(
                [("treatment_id", "=", record.id)]
            )

    @api.depends("diagnosis_line_id.diagnosis_type", "treatment_date")
    def _compute_has_high_diagnosis_past(self):
        today = date.today()
        for record in self:
            record.has_high_diagnosis_past = any(
                diagnosis.diagnosis_type == "high" for diagnosis in record.diagnosis_line_id
            ) and record.treatment_date <= today

    def action_open_sale_orders(self):
        return {
            "name": "Sales Orders",
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "view_mode": "tree,form",
            "domain": [("treatment_id", "=", self.id)],
            "context": {"default_treatment_id": self.id},
        }

    def action_download_blank_report(self):
        return self.env.ref(
            "codetrade_hospital.hospital_treatment_report_action"
        ).report_action(self)

    @api.constrains("diagnosis_line_id")
    def _check_high_diagnosis(self):
        for record in self:
            high_count = sum(
                1 for line in record.diagnosis_line_id if line.diagnosis_type == "high"
            )
            if high_count > 1:
                raise ValidationError(
                    "The diagnosis type 'high' can only be selected once per treatment."
                )
    @api.model
    def _auto_mark_done(self):
        treatments = self.search([("state", "=", "active")])
        for treatment in treatments:
            treatment.set_done()

