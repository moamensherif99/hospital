from datetime import date
from odoo import models,fields,api,_
from datetime import timedelta
from odoo.exceptions import ValidationError

class AppointmenReportWizard(models.TransientModel):
    _name = 'appointment.report.wizard'
    _description = 'Appointment Report Wizard'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    start_date = fields.Date(string='Start Date', required=0)
    end_date = fields.Date(string='End Date', required=0)

    def action_generate_report(self):
        domain = []
        patient_id = self.patient_id
        if patient_id:
            domain.append(('patient_id', '=', patient_id.id))
        if self.start_date:
            domain.append(('booking_date', '>=', self.start_date))
        if self.end_date:
            domain.append(('booking_date', '<=', self.end_date))

        # appointments = self.env['hospital.appointment'].search_read(domain)
        appointments = self.env['hospital.appointment'].search(domain)
        data_appointments = []
        for appointment in appointments:
            data_appointments.append({
                'ref': appointment.ref,
                'age': appointment.patient_id.age,
            })


        data = {
            'form_data': self.read()[0],
            'appointments': data_appointments,
        }
        print(appointments)

        return self.env.ref('om_hospital.report_patient_appointment_wizard_id').report_action(self, data=data)

    def action_generate_xls_report(self):

        domain = []
        patient_id = self.patient_id
        if patient_id:
            domain.append(('patient_id', '=', patient_id.id))
        if self.start_date:
            domain.append(('booking_date', '>=', self.start_date))
        if self.end_date:
            domain.append(('booking_date', '<=', self.end_date))

        appointments = self.env['hospital.appointment'].search(domain)
        data_appointments = []
        for appointment in appointments:
            data_appointments.append({
                'ref': appointment.ref,
                'name': appointment.patient_id.name,
            })
        data = {
            'form_data': self.read()[0],
            'appointments': data_appointments,
        }

        return self.env.ref('om_hospital.report_patient_appointment_id_xlsx').report_action(self, data=data)
