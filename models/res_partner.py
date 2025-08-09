from odoo import models, fields , api 

class ResPartner(models.Model):
    _inherit = 'res.partner'
    is_library_member = fields.Boolean(string="Is Library Member", default=False)
    card_id = fields.Char(string="Library Card ID", readonly=True)

    library_memberships_count = fields.Integer(string="Memberships Count", compute="_compute_memberships_count")

    def _compute_memberships_count(self):
        for partner in self:
            partner.library_memberships_count = self.env['library.membership'].search_count([('partner_id', '=', partner.id)])

    def action_view_library_memberships(self):
        self.ensure_one()
        return {
            'name': 'Membership Requests',
            'type': 'ir.actions.act_window',
            'res_model': 'library.membership',
            'domain': [('partner_id', '=', self.id)],
            'view_mode': 'list,form',
            'target': 'current',
        }
