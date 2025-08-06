from datetime import date
from odoo import models,fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users')
    customer_country_name = fields.Char(related='partner_id.country_id.name', string="Customer Country")

    def action_confirm(self):
        print('GGGGGGGGGGGGGGGG')
        super(SaleOrder,self).action_confirm()
        self.confirmed_user_id = self.env.user.id

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['so_confirmed_user_id'] = self.confirmed_user_id.id
        return invoice_vals

    @api.ondelete(at_uninstall=False)
    def _unlink_except_draft_or_cancel(self):
        pass


class SaleReport(models.Model):
    _inherit = 'sale.report'

    confirmed_user_id = fields.Many2one('res.users', string='Confirmed User', readyonly=True)

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['confirmed_user_id'] = "s.confirmed_user_id"
        return res
