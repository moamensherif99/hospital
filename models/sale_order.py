from datetime import date
from odoo import models,fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users')

    def action_confirm(self):
        print('GGGGGGGGGGGGGGGG')
        super(SaleOrder,self).action_confirm()
        self.confirmed_user_id = self.env.user.id
