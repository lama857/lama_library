from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta, date

class LibraryBorrowing(models.Model):
    _name = 'library.borrowing'
    _description = 'Borrowing Record'

    book_id = fields.Many2one('library.book', string='Book', required=True)
    borrower_id = fields.Many2one('res.partner', string='Borrower', required=True)
    card_id = fields.Char(string="Card ID", related='borrower_id.card_id', readonly=True)
    borrow_date = fields.Date(string='Borrow Date', default=fields.Date.context_today)
    return_date = fields.Date(string='Return Date', store=True)
    returned = fields.Boolean(string='Returned', default=False)

    @api.onchange('borrow_date')
    def _onchange_borrow_date(self):
        if self.borrow_date:
            self.return_date = self.borrow_date + timedelta(days=7)

    @api.onchange('borrower_id')
    def _onchange_borrower_id(self):
        if self.borrower_id:
            self.card_id = self.borrower_id.card_id

    @api.model
    def create(self, vals):
        partner = self.env['res.partner'].browse(vals['borrower_id'])
        membership = self.env['library.membership'].search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'active'),
            ('registration_date', '<=', date.today()),
            ('end_date', '>=', date.today()),
        ], limit=1)
        if not membership:
            raise ValidationError("Borrower does not have an active membership valid for today.")

        book = self.env['library.book'].browse(vals['book_id'])
        if not book.is_available:
            raise ValidationError("This book is already borrowed and not available.")
        
        record = super(LibraryBorrowing, self).create(vals)
        book.write({'is_available': False})
        return record

    def action_mark_returned(self):
        for record in self:
            if not record.returned:
                record.returned = True
            record.book_id.write({'is_available': True})

    @api.constrains('book_id')
    def _check_duplicate_borrowing(self):
        for record in self:
            ongoing = self.search([
                ('book_id', '=', record.book_id.id),
                ('returned', '=', False),
                ('id', '!=', record.id)
            ])
            if ongoing:
                raise ValidationError("This book is already borrowed and has not been returned yet.")