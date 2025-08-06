# -*- coding: utf-8 -*-
from odoo import models
from datetime import date

class PatientCardXLSX(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_card_xlsx'
    _description = 'Patient Card XLS Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        """
        Generates a professional multi-sheet Excel report for patient records.

        Args:
            workbook (xlsxwriter.Workbook): The workbook object.
            data (dict): The data dictionary passed from the report action.
            patients (recordset): The recordset of 'hospital.patient' to be reported.
        """
        # 1. Create a summary sheet for all patients
        self._create_summary_sheet(workbook, patients)

        # 2. Create a detailed sheet for each individual patient
        for patient in patients:
            self._create_patient_detail_sheet(workbook, patient)

    def _create_summary_sheet(self, workbook, patients):
        """Creates the summary worksheet with a list of all patients."""
        # Add a worksheet for the summary
        sheet = workbook.add_worksheet('Patient Summary')

        # Define cell formats
        title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#DDEBF7'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#F2F2F2', 'border': 1, 'align': 'center'})
        cell_format = workbook.add_format({'border': 1})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'border': 1})

        # Set column widths
        sheet.set_column('A:A', 30)  # Patient Name
        sheet.set_column('B:B', 15)  # Reference
        sheet.set_column('C:C', 8)   # Age
        sheet.set_column('D:D', 10)  # Gender
        sheet.set_column('E:E', 15)  # Create Date
        sheet.set_column('F:F', 40)  # Tags

        # Write Title
        sheet.merge_range('A1:F2', 'Patient Summary Report', title_format)

        # Write Headers
        headers = ['Patient Name', 'Reference', 'Age', 'Gender', 'Create Date', 'Tags']
        for col, header in enumerate(headers):
            sheet.write(3, col, header, header_format)

        # Write Data Rows
        row = 4
        for patient in patients:
            sheet.write(row, 0, patient.name, cell_format)
            sheet.write(row, 1, patient.ref, cell_format)
            sheet.write(row, 2, patient.age, cell_format)
            sheet.write(row, 3, dict(patient._fields['gender'].selection).get(patient.gender), cell_format)
            sheet.write(row, 4, patient.create_date.date(), date_format)
            # Join many2many tag names into a single string
            tags = ', '.join(tag.name for tag in patient.tag_ids)
            sheet.write(row, 5, tags, cell_format)
            row += 1

    def _create_patient_detail_sheet(self, workbook, patient):
        """Creates a detailed worksheet for a single patient."""
        report_name = f"Card - {patient.name}"
        sheet = workbook.add_worksheet(report_name[:31]) # Sheet name limit is 31 chars

        # --- Define Formats ---
        title_format = workbook.add_format({'bold': True, 'font_size': 20, 'align': 'center', 'valign': 'vcenter', 'font_color': '#44546A'})
        ref_format = workbook.add_format({'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'font_color': '#595959'})
        section_header_format = workbook.add_format({'bold': True, 'font_size': 12, 'bg_color': '#DDEBF7', 'border': 1, 'align': 'center'})
        label_format = workbook.add_format({'bold': True, 'bg_color': '#F2F2F2', 'border': 1})
        value_format = workbook.add_format({'border': 1})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'border': 1})
        birthday_format = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#28a745', 'align': 'center', 'border': 1})

        # --- Set Column Widths ---
        sheet.set_column('A:A', 25) # Labels
        sheet.set_column('B:B', 40) # Values
        sheet.set_column('C:D', 25) # Labels
        sheet.set_column('E:E', 40) # Values

        # --- Report Header ---
        sheet.merge_range('A1:E2', 'Patient Card', title_format)
        sheet.merge_range('A3:E3', patient.ref, ref_format)

        # Birthday Wish Banner
        row = 4
        if patient.is_birth_date:
            sheet.merge_range(f'A{row}:E{row}', f"🎉 Wishing {patient.name} a Happy Birthday! 🎉", birthday_format)
            row += 1

        row += 1 # Add a spacer row

        # --- Personal Information Section ---
        sheet.merge_range(f'A{row}:E{row}', 'Personal Information', section_header_format)
        row += 1

        sheet.write(f'A{row}', 'Patient Name', label_format)
        sheet.write(f'B{row}', patient.name, value_format)
        sheet.write(f'A{row+1}', 'Date of Birth', label_format)
        sheet.write(f'B{row+1}', patient.date_of_birth, date_format)
        sheet.write(f'A{row+2}', 'Age', label_format)
        sheet.write(f'B{row+2}', f"{patient.age} years old", value_format)
        sheet.write(f'A{row+3}', 'Gender', label_format)
        sheet.write(f'B{row+3}', dict(patient._fields['gender'].selection).get(patient.gender), value_format)

        # --- Other Information Section ---
        row += 5 # Move down to start the next section
        sheet.merge_range(f'A{row}:E{row}', 'Other Information', section_header_format)
        row += 1

        # Contact Info
        sheet.write(f'A{row}', 'Phone', label_format)
        sheet.write(f'B{row}', patient.phone, value_format)
        sheet.write(f'A{row+1}', 'Email', label_format)
        sheet.write(f'B{row+1}', patient.email, value_format)
        sheet.write(f'A{row+2}', 'Website', label_format)
        sheet.write(f'B{row+2}', patient.website, value_format)

        # Marital Status
        sheet.write(f'D{row}', 'Marital Status', label_format)
        sheet.write(f'E{row}', dict(patient._fields['marital_status'].selection).get(patient.marital_status), value_format)
        if patient.marital_status == 'married':
            sheet.write(f'D{row+1}', 'Partner Name', label_format)
            sheet.write(f'E{row+1}', patient.partner_name, value_format)

        # Parent Info (conditional)
        if patient.age < 15 and patient.gender != 'male':
             sheet.write(f'D{row+2}', 'Parent Name', label_format)
             sheet.write(f'E{row+2}', patient.parent, value_format)

        # --- Tags and Appointments ---
        row += 4 # Move down
        sheet.merge_range(f'A{row}:E{row}', 'Medical Info', section_header_format)
        row += 1

        sheet.write(f'A{row}', 'Tags', label_format)
        sheet.merge_range(f'B{row}:E{row}', ', '.join(tag.name for tag in patient.tag_ids), value_format)

        sheet.write(f'A{row+1}', 'Appointment Count', label_format)
        sheet.merge_range(f'B{row+1}:E{row+1}', patient.appointment_count, value_format)

        # You could add a list of appointments here if needed
        # row += 2
        # sheet.write(f'A{row}', 'Appointments', label_format)
        # for app in patient.appointment_ids:
        #     sheet.write(f'B{row}', f"{app.name} on {app.date}", value_format)
        #     row += 1
