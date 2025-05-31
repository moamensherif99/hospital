from odoo import models,fields,api

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Patient'

    name = fields.Char(string='Name',tracking=1)
    active = fields.Boolean(string='Active',default=True)
    ref = fields.Char(string='Reference')
    age = fields.Integer(string='Age',tracking=1)
    gender = fields.Selection(
        [('male','Male'),
         ('female','Female')],string='Gender',tracking=1
    )