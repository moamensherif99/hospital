from datetime import date
from odoo import models,fields,api,_
from datetime import timedelta
from odoo.exceptions import ValidationError

class PatientReporttWizard(models.TransientModel):
    _name = 'patient.report.wizard'
    _description = 'Patient Report Wizard'

    gender = fields.Selection(
        [('male', 'Male'),
         ('female', 'Female')], string='Gender')
    age = fields.Integer(string='Age')


    def action_print_report(self):
        data = {
            'form_data': self.read()[0],
        }
        return self.env.ref('om_hospital.report_patient_wizard_id').report_action(self, data=data)
