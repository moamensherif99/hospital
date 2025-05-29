from odoo import models,fields,api

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active',default=True)
    ref = fields.Char(string='Reference')
    age = fields.Integer(string='Age')
    gender = fields.Selection(
        [('male','Male'),
         ('female','Female')],string='Gender'
    )