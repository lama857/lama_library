from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random

class LibraryMembership(models.Model):
    _name = 'library.membership'
    _description = 'Library Membership Request'

    partner_id = fields.Many2one(
        'res.partner',
        string='Member',
        required=True,
        domain="[('is_library_member','=',False)]"
    )
    invoice_id = fields.Many2one('account.move', string="Invoice")
    registration_date = fields.Date(string="Registration Date", default=fields.Date.today)
    end_date = fields.Date(string="End Date")
    card_id = fields.Char(string="Card ID", readonly=True)
    payment_terms = fields.Selection([
        ('cash', 'Cash'),
        ('installment', 'Installment'),
    ], string="Payment Terms", default='cash')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('active', 'Active'),
    ], default='draft', string="Status")

    membership_lines = fields.One2many('library.membership.line', 'membership_id', string='Membership Lines')

    def action_confirm(self):
        for rec in self:
            if not rec.membership_lines:
                raise ValidationError("You must add at least one membership line before confirming.")
            
            invoice_lines = []
            for line in rec.membership_lines:
                invoice_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.product_id.name,
                    'quantity': 1,
                    'price_unit': line.amount,
                    'tax_ids': [(6, 0, line.product_id.taxes_id.ids)],
                }))
            
            invoice = self.env['account.move'].create({
                'partner_id': rec.partner_id.id,
                'move_type': 'out_invoice',  
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': invoice_lines,
            })

            rec.invoice_id = invoice.id
            rec.state = 'confirmed'

    def action_mark_paid(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise ValidationError("Membership must be confirmed before marking as paid.")
            if not rec.invoice_id:
                raise ValidationError("No invoice found for this membership.")
            if rec.invoice_id.payment_state != 'paid':
                raise ValidationError("Invoice must be fully paid before marking membership as paid.")
            
            rec.state = 'paid'
            rec.card_id = 'CARD-' + str(random.randint(1000, 9999))
            rec.partner_id.card_id = rec.card_id
            rec.partner_id.is_library_member = True
            rec.action_activate_membership()

    def action_activate_membership(self):
        for rec in self:
            if rec.state != 'paid':
                raise ValidationError("Membership must be paid before activation.")
            rec.state = 'active'

    def action_view_invoice(self):
        self.ensure_one()
        if self.invoice_id:
            return {
                'name': 'Invoice',
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': self.invoice_id.id,
                'view_mode': 'form',
            }

    def print_single_membership_report(self):
        self.ensure_one()
        return self.env.ref('lama_library.action_report_single_memberships').report_action(self)

    def print_multiple_membership_report(self):
        return self.env.ref('lama_library.action_report_multiple_memberships').report_action(self)
