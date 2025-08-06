from odoo import api, fields, models
import base64
import io

class PatientAppointmentXLS(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_appointment_xlsx'
    _description = 'Patient Appointment XLS Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
      print(data['appointments'])
      sheet = workbook.add_worksheet('Patient Appointment Report')
      bold = workbook.add_format({'bold': True})
      row = 3
      col = 3
      sheet.write(row, col, "Ref", bold)
      sheet.write(row, col + 1, "Patient Name", bold)
      sheet.set_column('D:E', 30)
      for appointment in data['appointments']:
            row += 1
            sheet.write(row, col, appointment['ref'])
            sheet.write(row, col + 1, appointment['name'])

