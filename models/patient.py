from datetime import date
from odoo import models,fields,api

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Patient'

    name = fields.Char(string='Name',tracking=1)
    active = fields.Boolean(string='Active',default=True)
    ref = fields.Char(string='Reference')
    date_of_birth = fields.Date(tracking=1)
    age = fields.Integer(compute='_compute_age', string='Age',store=1 , tracking=1)
    gender = fields.Selection(
        [('male','Male'),
         ('female','Female')],string='Gender',tracking=1
    )
    appointment_id = fields.Many2one('hospital.appointment', string='Appointments')

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0
