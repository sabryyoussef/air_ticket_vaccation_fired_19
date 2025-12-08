from odoo import models, fields

class ExitEntryAttachment(models.Model):
    _name = 'exit.entry.attachment'
    _description = 'Exit and Re-entry Request Attachment'
    
    exit_entry_id = fields.Many2one('hr.exit.entry.request', string="Exit and Re-entry Request", ondelete="cascade")
    name = fields.Char(string="Name", required=True)
    file = fields.Binary(string="File", required=True)
    file_name = fields.Char(string="File Name")
    note = fields.Char(string="Note")
    active = fields.Boolean(string='Active', default=True)