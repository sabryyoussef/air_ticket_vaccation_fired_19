from odoo import models, fields, api, _


class HrLeave(models.Model):
    _inherit = 'hr.leave'
    
    air_ticket_id = fields.Many2one('air.ticket.request', string='Linked Air-Ticket')