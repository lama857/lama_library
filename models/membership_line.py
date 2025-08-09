from odoo import models, fields ,api 

class LibraryMembershipLine(models.Model):
    _name = 'library.membership.line'
    _description = 'Membership Line'

    membership_id = fields.Many2one('library.membership', string="Membership")
    product_id = fields.Many2one('product.product', string='Membership Product')
    amount = fields.Monetary('Amount')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)  
