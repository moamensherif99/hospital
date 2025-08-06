from datetime import date
from odoo import models,fields,api

class PatientTag(models.Model):
    _name = 'patient.tag'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Tag'

    name = fields.Char(string='Name',tracking=1, trim=0)
    active = fields.Boolean(string='Active',default=True)
    color = fields.Integer(string='Color Index', default=0)
    color_2 = fields.Char(copy=False)
    sequence = fields.Integer(string='Sequence', default=10, help="Used to order tags in the kanban view.")

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Only one tag can exist with a specific tag_name'),
        ('required_sequence', 'CHECK(sequence > 0)', 'sequence must be greater than zero!')
    ]

    # def copy(self, default=None):
    #     if default is None:
    #         default = {}
    #     if not default.get('name'):
    #         default['name'] = f"{self.name} (copy)"
    #     return super(PatientTag,self).copy(default)

    def copy(self, default=None):
        """
        Ensures that duplicating a record creates a unique name
        by appending "(copy)" or "(copy N)"
        """
        if default is None:
            default = {}
        if not default.get('name'):
            copied_name = f"{self.name} (copy)"
            record_count = self.search_count([('name', '=', copied_name)])
            copy_number = 2
            while record_count > 0:
                copied_name = f"{self.name} (copy {copy_number})"
                record_count = self.search_count([('name', '=', copied_name)])
                copy_number += 1
            default['name'] = copied_name
        return super(PatientTag, self).copy(default)
