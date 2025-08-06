import typing
from datetime import date
from re import search

from dateutil.relativedelta import relativedelta
from importlib.metadata import requires

from reportlab.graphics.transform import inverse

from odoo import models, fields, api, _
from odoo.api import IdType, Self
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Patient'
    _rec_name = 'name'

    name = fields.Char(string='Name', tracking=1)
    active = fields.Boolean(string='Active', default=True)
    ref = fields.Char(string='Reference', default='New', readonly=True, tracking=1)
    date_of_birth = fields.Date(tracking=1)
    is_birth_date = fields.Boolean(string='Is Birth Date', compute='_compute_is_birth_date')
    age = fields.Integer(compute='_compute_age', inverse='inverse_compute_age', string='Age', store=1, tracking=1)
    gender = fields.Selection(
        [('male', 'Male'),
         ('female', 'Female')], string='Gender', tracking=1
    )
    male_power = fields.Char()
    appointment_id = fields.Many2one('hospital.appointment', string='Appointments')
    image = fields.Image()
    tag_ids = fields.Many2many('patient.tag', string='Tags', tracking=1)
    display_name = fields.Char(compute='_compute_display_name', store=True)
    appointment_count = fields.Integer(compute='_compute_appointment_count', string='Appointment Count', store=True,
                                       tracking=1)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    parent = fields.Char(string='Parent/Guardian Name', tracking=1)
    marital_status = fields.Selection(
        [('single', 'Single'),
         ('married', 'Married'),
         ('divorced', 'Divorced'),
         ('widowed', 'Widowed')],
    )
    partner_name = fields.Char(string='Partner Name', tracking=1)
    phone = fields.Char(string='Phone', tracking=1)
    email = fields.Char(string='Email', tracking=1)
    website = fields.Char(string='Website', tracking=1)

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > date.today():
                raise ValidationError(_("Date of birth cannot be in the future."))

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends('age')
    def inverse_compute_age(self):
        for rec in self:
            if rec.age and rec.date_of_birth:
                rec.date_of_birth = date.today() - relativedelta(years=rec.age)
            elif rec.age:
                rec.date_of_birth = date.today() - relativedelta(years=rec.age)
            else:
                rec.date_of_birth = False

    # @api.depends('date_of_birth')
    # def _compute_age(self):
    #     for rec in self:
    #         if rec.date_of_birth:
    #             today = date.today()
    #             delta = relativedelta(today, rec.date_of_birth)
    #             rec.age = delta.years
    #         else:
    #             rec.age = 0
    #
    # @api.depends('age')
    # def inverse_compute_age(self):
    #     for rec in self:
    #         if rec.age:
    #             rec.date_of_birth = date.today() - relativedelta(years=rec.age)
    #         else:
    #             rec.date_of_birth = False

    @api.depends('name', 'ref')
    def _compute_display_name(self):
        for rec in self:
            # You can add logic here in case a field is empty
            if rec.ref:
                rec.display_name = f"{rec.name} ({rec.ref})"
            else:
                rec.display_name = rec.name

    # @api.depends('appointment_ids')
    # def _compute_appointment_count(self):
    #     for rec in self:
    #         rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        # Perform a single read_group query to get the count of appointments for all relevant patients
        appointment_group = self.env['hospital.appointment'].read_group(
            domain=[('patient_id', 'in', self.ids)],
            fields=['patient_id'],
            groupby=['patient_id']
        )

        # Create a dictionary mapping each patient_id to its appointment count
        mapped_data = {data['patient_id'][0]: data['patient_id_count'] for data in appointment_group}

        # Loop through the patient records and assign the computed count
        for rec in self:
            # Use .get() with a default of 0 for patients who have no appointments
            rec.appointment_count = mapped_data.get(rec.id, 0)

    # @api.depends('appointment_ids')
    # def _compute_appointment_count(self):
    #     for rec in self:
    #         rec.appointment_count = len(rec.appointment_ids)

    @api.depends('date_of_birth')
    def _compute_is_birth_date(self):
        today = date.today()
        for rec in self:
            # Default to False
            is_birthday_today = False
            if rec.date_of_birth:
                # Check if the month and day match today's month and day
                if rec.date_of_birth.month == today.month and rec.date_of_birth.day == today.day:
                    is_birthday_today = True
            rec.is_birth_date = is_birthday_today

    def action_view_appointments(self):
        self.ensure_one()
        return {
            'name': _('Appointments'),
            'view_mode': 'list,form,calendar',
            'res_model': 'hospital.appointment',
            'type': 'ir.actions.act_window',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            # 'context': {'create': False},
        }

    @api.model
    def create(self, vals):
        res = super(HospitalPatient, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('patient_seq')
        return res

    def write(self, vals):
        res = super(HospitalPatient, self).write(vals)
        print('nice')
        return res

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("You cannot delete a patient with existing appointments."))

    def action_test(self):
        print("This is a test action for the patient model.")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Good Job!'}}

    def get_patient_vcard_qr_data(self):
        self.ensure_one()
        vcard_data = f"BEGIN:VCARD\n" \
                     f"VERSION:3.0\n" \
                     f"N:{self.name}\n" \
                     f"FN:{self.name}\n" \
                     f"TEL:{self.phone or ''}\n" \
                     f"EMAIL:{self.email or ''}\n" \
                     f"END:VCARD"
        return vcard_data
