# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)

        for move in res:
            if move.product_tmpl_id:
                move.product_tmpl_id.last_stock_move_date = move.date

        return res

    def write(self, vals):
        res = super().write(vals)

        for move in self:
            if move.state == 'done' and move.date and move.product_tmpl_id:
                move.product_tmpl_id.last_stock_move_date = move.date

        return res
