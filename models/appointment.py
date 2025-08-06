from email.policy import default
import urllib.parse
import random

from reportlab.lib.randomtext import subjects

from odoo import models, fields, api, _
from odoo.api import ondelete
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'
    _order = 'id desc'

    # patient_id = fields.Many2one('hospital.patient', ondelete='restrict', string='Patient')
    patient_id = fields.Many2one('hospital.patient', ondelete='cascade', string='Patient')
    ref = fields.Char(string='Reference', related='patient_id.ref')
    appointment_time = fields.Datetime(default=fields.Datetime.now)
    booking_date = fields.Date(default=fields.Date.today)
    gender = fields.Selection(related='patient_id.gender')
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([('0', 'Normal'),
                                 ('1', 'Low'),
                                 ('2', 'High'),
                                 ('3', 'Very High')], string='Priority')
    state = fields.Selection([('draft', 'Draft'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')], default="draft", string="Status")
    doctor_id = fields.Many2one('res.users', string='Doctor')
    appointment_pharmacy_lines_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id',
                                                     string='Pharmacy Lines')
    hide_sales_price = fields.Boolean(string='Hide Sales Price')
    operation_id = fields.Many2one('hospital.operation', string='Operation')
    progress = fields.Integer(string='Progress', compute='_compute_progress', store=True, tracking=True)
    duration = fields.Float(string='Duration')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True)
    amount_total = fields.Monetary(string='Total', store=True, compute='_compute_amount_all', tracking=True)

    def action_test(self):
        # url_action
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://www.youtube.com/',
            'target': 'new',

        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'
            else:
                raise ValidationError(_("You can only change the state to In Consultation from Draft."))

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Good Jop!',
                'type': 'rainbow_man',
            }
        }
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                rec.progress = random.randrange(0, 26)
            elif rec.state == 'in_consultation':
                rec.progress = random.randrange(25, 100)
            elif rec.state == 'done':
                rec.progress = 100
            else:
                rec.progress = 0

    def action_cancel(self):
        action = self.env.ref('om_hospital.cancel_appointment_action').read()[0]
        for rec in self:
            rec.state = 'cancel'
        return action

    def action_smart_patient(self):
        querry = """select id,name from hospital_patient order by id asc"""
        self.env.cr.execute(querry)
        # result = self.env.cr.fetchall() # Fetch all results in a list of tuples
        # result = self.env.cr.fetchone()  # Fetch one result as a tuple
        # result = self.env.cr.fetchmany(10)  # Fetch a specified number of results as a list of tuples
        result = self.env.cr.dictfetchall()  # Fetch all results as a list of dictionaries
        # result = self.env.cr.dictfetchone()
        print(result)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Patient Details'),
            'res_model': 'hospital.patient',
            'res_id': self.patient_id.id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': self.env.context,
            'flags': {'form': {'action_buttons': True}},  # Optional: shows action buttons in popup
        }

    def action_notification(self):
        action = self.env.ref('om_hospital.patient_action')  # لازم يكون action form
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Info On Patient"),
                'message': '%s',
                'links': [{
                    'label': self.patient_id.name,
                    'url': f"/web#action={action.id}&id={self.patient_id.id}&model=hospital.patient&view_type=form",
                }],
                'sticky': False,
            }
        }

    # def action_notification(self):
    #     action = self.env.ref('om_hospital.patient_action')  # لازم يكون action form
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'display_notification',
    #         'params': {
    #             'title': _("Info On Patient"),
    #             'message': '%s',
    #             'links': [{
    #                 'label': self.patient_id.name,
    #                 'url': f"/web#action={action.id}&id={self.patient_id.id}&model=hospital.patient&view_type=form",
    #             }],
    #             'sticky': False,
    #             'next': {
    #                 'type': 'ir.actions.act_window',
    #                 'res_model': 'hospital.patient',
    #                 'res_id': self.patient_id.id,
    #                 'views': [[False, 'form']],
    #                 'target': 'current',
    #             },
    #         }
    #     }

    def action_share_whatsapp(self):
        for rec in self:
            phone_number = rec.patient_id.phone
            if not phone_number:
                raise ValidationError(_("The patient does not have a phone number."))
            message = f"\n*Appointment Details:*\nPatient: {rec.patient_id.name}\nDate: {rec.booking_date}\nTime: {rec.appointment_time}"
            encoded_message = urllib.parse.quote(message)  # Encode the message for URL
            whatsapp_url = f"https://api.whatsapp.com/send?phone={phone_number}&text={message}"
            self.message_post(body=message)
            return {
                'type': 'ir.actions.act_url',
                'url': whatsapp_url,
                'target': 'new',
            }

    def action_send_email(self):
        template = self.env.ref('om_hospital.appointment_mail_template')
        for rec in self:
            if rec.patient_id.email:
                template.send_mail(rec.id, force_send=True)
            else:
                raise ValidationError(_("The patient does not have an email address."))

    @api.depends('appointment_pharmacy_lines_ids.price_subtotal')  # <-- CORRECTED
    def _compute_amount_all(self):
        for rec in self:
            rec.amount_total = sum(line.price_subtotal for line in rec.appointment_pharmacy_lines_ids)  # <-- CORRECTED

    def set_line_number(self):
        sl_no = 0
        for line in self.appointment_pharmacy_lines_ids:
            sl_no += 1
            line.sl_no = sl_no

    @api.model
    def create(self, vals):
        res = super(HospitalAppointment, self).create(vals)
        res.set_line_number()
        return res

    def write(self, vals):
        res = super(HospitalAppointment, self).write(vals)
        self.set_line_number()
        return res

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_("You can only delete an appointment that is in state Draft."))
        return super(HospitalAppointment, self).unlink()


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    price_unit = fields.Float(string='Price', related='product_id.list_price', digits='Product Price')
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    currency_id = fields.Many2one('res.currency', string='Currency', related='appointment_id.currency_id',
                                  readonly=True)
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_price_subtotal', store=True,
                                     currency_field='currency_id')
    sl_no = fields.Integer(string='Serial No')

    @api.depends('price_unit', 'qty')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.qty
