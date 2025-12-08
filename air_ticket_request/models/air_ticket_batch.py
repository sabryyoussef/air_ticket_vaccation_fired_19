from odoo import models, fields, api
from odoo.exceptions import UserError

class AirTicketRequestBatch(models.Model):
    _name = 'air.ticket.request.batch'
    _description = 'Air Ticket Request Batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Batch Name', required=True, default='New')
    date = fields.Date(string='Date', default=fields.Date.today, required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, 
                                default=lambda self: self.env.company)
    
    state = fields.Selection([
        ('new', 'New'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('refused', 'Refused')
    ], string='Status', default='new', tracking=True)
    
    request_ids = fields.One2many('air.ticket.request', 'batch_id', string='Air Ticket Requests')
    attachment_ids = fields.One2many('ir.attachment', 'res_id', string='Attachments',
                                   domain=[('res_model', '=', 'air.ticket.request.batch')])
    note = fields.Text(string='Notes')
    
    count_requests = fields.Integer(string='Number of Requests', compute='_compute_counts')
    active = fields.Boolean(string='Active', default=True)
    
    @api.depends('request_ids')
    def _compute_counts(self):
        for batch in self:
            batch.count_requests = len(batch.request_ids)
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('air.ticket.request.batch') or 'New'
        return super().create(vals)
    
    def review(self):
        for batch in self:
            batch.write({'state': 'reviewed'})
    
    def approve(self):
        for batch in self:
            batch.write({'state': 'approved'})
            # يمكن إضافة منطق الموافقة على الطلبات المرتبطة هنا
    
    def refuse(self):
        for batch in self:
            batch.write({'state': 'refused'})
    
    def reset(self):
        for batch in self:
            batch.write({'state': 'new'})
    
    def refresh(self):
        for batch in self:
            # منطق تحديث البيانات
            pass
    
    def generate_requests(self):
        for batch in self:
            # منطق توليد طلبات التذاكر تلقائياً
            # يمكن البحث عن الموظفين المؤهلين وإنشاء طلبات لهم
            pass
    
    def open_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Air Ticket Requests',
            'res_model': 'air.ticket.request',
            'view_mode': 'tree,form',
            'domain': [('batch_id', '=', self.id)],
            'context': {'default_batch_id': self.id}
        }