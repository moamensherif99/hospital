# -*- coding: utf-8 -*-
from email.policy import default

from odoo import fields, models, api


class HospitalOperation(models.Model):
    _name = 'hospital.operation'
    _description = 'Hospital Operation'
    _log_access = False
    _order = 'sequence, id'

    doctor_id = fields.Many2one('res.users', string='Doctor')
    operation_name = fields.Char(string='Name')
    reference_record = fields.Reference([('hospital.patient','Patient'),('hospital.appointment','Appointment')], string='Record')
    #Reference will store the data in the database as string
    sequence = fields.Integer(default=10)

    @api.model
    def name_create(self, name):
        rec = self.create({'operation_name': name})
        return rec.id, rec.operation_name
    #use this function to create a new operation with a name if u dont want to use name or _rec_name
