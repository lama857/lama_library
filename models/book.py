from odoo import models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char(string='Title', required=True)
    author_id = fields.Many2one('library.author', string='Author')
    description = fields.Text(string='Description')
    publish_date = fields.Date(string='Publish Date')
    is_available = fields.Boolean(string='Available', default=True)
