# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    last_stock_move_date = fields.Datetime(
        string="Last Stock Move Date",
        readonly=True,
    )
