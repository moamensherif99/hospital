from odoo import models, fields, api

class AllPatientReport(models.AbstractModel):
    #_name = 'report.module_name.template_name'
    _name = 'report.om_hospital.report_patient_wizard_template'
    _description = 'All Patient Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        Fetches the report values for all patients.

        Args:
            docids (list): List of patient IDs.
            data (dict, optional): Additional data for the report.

        Returns:
            dict: Contains the list of patients and other report data.
        """
        # Fetch all patients
        print(docids, data)
        domain = []
        gender = data.get('form_data').get('gender')
        if gender:
            domain += [('gender', '=', gender )]
        age = data.get('form_data').get('age')
        if age != 0:
            domain += [('age', '=', age)]

        docs = self.env['hospital.patient'].search(domain)

        return {
            'docs': docs,
        }