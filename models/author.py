from odoo import models, fields,api

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Author'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    book_ids = fields.One2many('library.book', 'author_id', string='Books')
