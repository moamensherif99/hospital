from email.policy import default

from odoo import models,fields,api

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hospital.patient')
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
            rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'