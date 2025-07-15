from datetime import date
from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', domain=[('priority','in',('0','1'))], readonly=False, required=True)
    reason = fields.Text(required=True)
    date_cancel = fields.Date(string='Cancellation Date', required=True)

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        return res

    def action_cancel(self):
        for rec in self:
            if rec.date_cancel > date.today():
                raise ValidationError(_("Cancellation date cannot be in the future."))
            else:
                rec.appointment_id.state = 'cancel'
