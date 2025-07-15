# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cancel_days = fields.Integer(string='Cancel Days', default=3, config_parameter='om_hospital.cancel_days', help="Number of days before an appointment can be cancelled.")
