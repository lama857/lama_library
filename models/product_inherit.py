from odoo import models, fields , api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_membership_product = fields.Boolean(string="Is Membership Product")