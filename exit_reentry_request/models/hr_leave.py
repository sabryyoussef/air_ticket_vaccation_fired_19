from odoo import models, fields, api, _


class HrLeave(models.Model):
    _inherit = 'hr.leave'
    
    linked_exit_renry_id = fields.Many2one('air.ticket.request', string='Air Ticket Request')