import base64
from io import BytesIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import xlsxwriter


class InvoiceReportWizard(models.TransientModel):
    _name = "invoice.report.wizard"
    _description = "Invoice Report Wizard"

    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)

    @api.constrains("from_date", "to_date")
    def _check_date_order(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise UserError(_("The 'From Date' cannot be later than the 'To Date'."))

    def generate_excel_report(self):
        if self.from_date > self.to_date:
            raise UserError(_("The 'From Date' cannot be later than the 'To Date'."))

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet("Invoice Report")

        bold_format = workbook.add_format({"bold": True})
        currency_format = workbook.add_format({"num_format": "#,##0.00"})
        subtotal_format = workbook.add_format({"bold": True, "bg_color": "#FFFF00"})

        headers = [
            "Customer",
            "Invoice Number",
            "Product",
            "Quantity",
            "Taxes",
            "Subtotal",
        ]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, bold_format)

        invoices = self.env["account.move"].search(
            [
                ("move_type", "=", "out_invoice"),
                ("invoice_date", ">=", self.from_date),
                ("invoice_date", "<=", self.to_date),
            ],
            order="partner_id, id",
        )

        row = 1
        total = 0.0
        current_customer = None

        for invoice in invoices:
            customer = invoice.partner_id.name or ""
            if customer != current_customer:
                worksheet.write(row, 0, customer)
                current_customer = customer

            for line in invoice.invoice_line_ids:
                worksheet.write(row, 1, invoice.name or "")
                worksheet.write(row, 2, line.product_id.name or "")
                worksheet.write(row, 3, line.quantity)
                worksheet.write(
                    row,
                    4,
                    (
                        ", ".join([f"{tax.amount}%" for tax in line.tax_ids])
                        if line.tax_ids
                        else "0%"
                    ),
                )
                worksheet.write(row, 5, line.price_subtotal, currency_format)
                row += 1

            total += invoice.amount_total

        worksheet.write(row + 1, 4, "Total:", bold_format)
        worksheet.write(row + 1, 5, total, subtotal_format)

        workbook.close()
        output.seek(0)

        file_data = base64.b64encode(output.read())
        output.close()

        attachment = self.env["ir.attachment"].create(
            {
                "name": "Invoice Report.xlsx",
                "type": "binary",
                "datas": file_data,
                "store_fname": "Invoice_Report.xlsx",
                "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
        )

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "new",
        }
