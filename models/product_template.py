# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.rec'


    last_stock_move_date = fields.Datetime(
        string="Last Stock Move Date",
        compute="_compute_last_stock_move_date",
        readonly=True,
        store=True,
    )

    def _compute_last_stock_move_date(self):
        for rec in self:
            last_move = self.env['stock.move'].search([
                ('product_id.product_tmpl_id', '=', rec.id),
                ('state', '=', 'done')
            ], order='date desc', limit=1)

            rec.last_stock_move_date = last_move.date if last_move else False
