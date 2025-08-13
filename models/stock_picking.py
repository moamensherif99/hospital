from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()

        for rec in self:
            if rec.date_done:
                for move in rec.move_ids:
                    if move.product_tmpl_id:
                        move.product_tmpl_id.last_stock_move_date = rec.date_done

        return res
