from email.policy import default

from odoo import models,fields,api,_
from odoo.api import ondelete
from odoo.exceptions import ValidationError

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'

    # patient_id = fields.Many2one('hospital.patient', ondelete='restrict', string='Patient')
    patient_id = fields.Many2one('hospital.patient', ondelete='cascade', string='Patient')
    ref = fields.Char(string='Reference',related='patient_id.ref')
    appointment_time = fields.Datetime(default=fields.Datetime.now)
    booking_date = fields.Date(default=fields.Date.today)
    gender = fields.Selection(related='patient_id.gender' )
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([('0', 'Normal'),
                                 ('1', 'Low'),
                                 ('2', 'High'),
                                 ('3', 'Very High')], string='Priority')
    state = fields.Selection([('draft', 'Draft'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')],default="draft", string="Status")
    doctor_id = fields.Many2one('res.users', string='Doctor')
    appointment_pharmacy_lines_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    hide_sales_price = fields.Boolean(string='Hide Sales Price')

    def action_test(self):
        print("This is a test action for the appointment model.")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Good Jop!',
                'type': 'rainbow_man',
            }
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

    def action_cancel(self):
        action = self.env.ref('om_hospital.cancel_appointment_action').read()[0]
        for rec in self:
            rec.state = 'cancel'
        return action

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_("You can only delete an appointment that is in state Draft."))
        return super(HospitalAppointment, self).unlink()


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    price_unit = fields.Float(string='Price', related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')