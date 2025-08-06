from odoo import api, fields, models
import base64
import io

class PatientCardXLS(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_card_xlsx'
    _description = 'Patient Card XLS Report'
    _inherit = 'report.report_xlsx.abstract'

    # def generate_xlsx_report(self, workbook, data, patients):
    #     for obj in patients:
    #         report_name = obj.name
    #         # One sheet by partner
    #         sheet = workbook.add_worksheet(report_name[:31])
    #         bold = workbook.add_format({'bold': True})
    #         sheet.write(0, 0, obj.name, bold)

    def generate_xlsx_report(self, workbook, data, patients):
        # Create a summary sheet for all patients in one sheet
        sheet = workbook.add_worksheet('Patient Card Report')
        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#DDEBF7'})
        row = 3
        col = 3
        sheet.set_column('D:E', 30)
        for obj in patients:
            row += 1
            sheet.merge_range(row, col, row, col + 1, "ID CARD", format_1)
            row += 1
            if obj.image:
                patient_image = io.BytesIO(base64.b64decode(obj.image))
                sheet.insert_image(row, col, f"{obj.name}_image.png", {'image_data': patient_image, 'x_scale': 0.1, 'y_scale': 0.1})
                row += 5
            row += 1
            sheet.write(row, col, "Name", bold)
            sheet.write(row, col + 1, obj.name)
            row += 1
            sheet.write(row, col, "Age", bold)
            sheet.write(row, col + 1, obj.age)
            row += 1
            sheet.write(row, col, "Reference", bold)
            sheet.write(row, col + 1, obj.ref)

            row += 2
