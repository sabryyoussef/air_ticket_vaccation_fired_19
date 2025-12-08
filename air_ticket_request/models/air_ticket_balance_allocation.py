from odoo import models, fields, api

class AirTicketBalanceAllocation(models.Model):
    _name = "air.ticket.balance.allocation"
    _description = "Air Ticket Balance Allocation"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, tracking=True)
    allocated_balance = fields.Float(string="Allocated Balance", required=True, tracking=True)
    allocated_date = fields.Date(string="Allocated Date", required=True, tracking=True)
    adjusted_date = fields.Date(string="Adjusted date", readonly=True)
    last_allocation_date = fields.Date(string="Last allocation date", readonly=True)
    reason = fields.Char(string="Reason", required=True)
    note = fields.Html(string="Notes")

    auto_create = fields.Boolean(string="Created automatically", readonly=True)
    air_ticket_auto_allocation_id = fields.Many2one('air.ticket.automatic.allocation', string="Automatic Allocation", readonly=True)
    air_ticket_request_id = fields.Many2one('air.ticket.request', string="Air Ticket Request", readonly=True)

    by_eos = fields.Boolean(string="Through EOS", readonly=True)
    # eos_id = fields.Many2one('employee.eos', string="EOS Request", readonly=True)

    confirmed_uid = fields.Many2one('res.users', string="Confirmed by", readonly=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    attachment_ids = fields.One2many('air.ticket.balance.attachment', 'air_ticket_balance_id', string="Attachments")

    state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
    ], string="Status", default='new', tracking=True)

    # ---------------------------------------------------------
    # Business Methods
    # ---------------------------------------------------------
    def confirm(self):
        for rec in self:
            rec.write({
                'state': 'confirmed',
                'confirmed_uid': self.env.user.id,  # Use .id instead of the user object
                'adjusted_date': fields.Date.today()  # Add this to set the adjustment date
            })

    def set_to_draft(self):
        for rec in self:
            rec.state = 'new'
            
from odoo import models, fields

class AirTicketBalanceAttachment(models.Model):
    _name = 'air.ticket.balance.attachment'
    _description = 'Air Ticket Balance Allocation Attachment'

    air_ticket_balance_id = fields.Many2one(
        'air.ticket.balance.allocation',
        string="Balance Allocation",
        ondelete="cascade"
    )
    file = fields.Binary(string="File", required=True)
    name = fields.Char(string="Name", required=True)
    file_name = fields.Char(string="File Name")
    note = fields.Char(string="Note")

