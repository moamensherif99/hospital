# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    def write(self, vals):

        product_templates_before = self.product_id.mapped('product_tmpl_id')
        res = super(StockMove, self).write(vals)
        product_templates_after = self.product_id.mapped('product_tmpl_id')
        all_product_templates = product_templates_before | product_templates_after

        if 'state' in vals or 'date' in vals:
            all_product_templates._compute_last_stock_move_date()

        return res

    @api.model_create_multi
    def create(self, vals):

        res = super(StockMove, self).create(vals)
        product_templates = res.product_id.mapped('product_tmpl_id')

        product_templates._compute_last_stock_move_date()

        return res
