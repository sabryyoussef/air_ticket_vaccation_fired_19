from odoo import models, fields, api, _

class AirTicketAutomaticAllocation(models.Model):
    _name = 'air.ticket.automatic.allocation'
    _description = 'Air Ticket Automatic Allocation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(string="Code", readonly=True, copy=False)
    name = fields.Char(string="Description", required=True, tracking=True)
    allocate_till_date = fields.Date(string="Allocate till this date", required=True)


    allocation_ids = fields.One2many(
        'air.ticket.balance.allocation',
        'air_ticket_auto_allocation_id',
        string="Balance allocations",
        readonly=True
    )

    count_allocation = fields.Integer(
        string="Allocations",
        compute="_compute_count_allocation"
    )

    confirmed_uid = fields.Many2one('res.users', string="Confirmed by", readonly=True)
    note = fields.Html(string="Notes")

    state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
    ], string="Status", default="new", tracking=True)

    # ----------------------------------------------------------------
    # Compute
    # ----------------------------------------------------------------
    def _compute_count_allocation(self):
        for rec in self:
            rec.count_allocation = len(rec.allocation_ids)

    # ----------------------------------------------------------------
    # Business Methods
    # ----------------------------------------------------------------
    def confirm(self):
        for rec in self:
            rec.state = 'confirmed'
            rec.confirmed_uid = self.env.user

    def action_set_to_new(self):
        for rec in self:
            rec.state = 'new'

    def open_allocations(self):
        """فتح سجل الـ Balance Allocations المرتبطة"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Balance Allocations'),
            'res_model': 'air.ticket.balance.allocation',
            'view_mode': 'tree,form',
            'domain': [('air_ticket_auto_allocation_id', '=', self.id)],
            'context': {'default_air_ticket_auto_allocation_id': self.id},
        }
    @api.model
    def create(self, vals): 
        if vals.get('code', 'New') == 'New': 
            vals['code'] = self.env['ir.sequence'].next_by_code('air.ticket.automatic.allocation') or 'New' 
        return super().create(vals)