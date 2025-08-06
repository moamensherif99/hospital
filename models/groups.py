from odoo import models,fields,api

class ResGroups(models.Model):
    _inherit = 'res.groups'


    def get_application_groups(self, domain):
        group_id = self.env.ref('product.group_product_pricelist').id
        wave_group = self.env.ref('base.group_allow_export').id
        return super(ResGroups, self).get_application_groups(domain + [('id', 'not in', (group_id, wave_group))])
    #this method is used to filter out the product pricelist and export groups from the application groups so user can not see them in the application menu