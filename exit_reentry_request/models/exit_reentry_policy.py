from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ExitReentryPolicy(models.Model):
    _name = "hr.exit.entry.type"
    _description = "Exit and Re-entry Policy"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "name asc"

    # Basic Information
    name = fields.Char(string="Description", required=True, tracking=True)
    code = fields.Char(string="Code", readonly=True, copy=False)
    
    # One Time Policy Section
    min_months = fields.Integer(string="Minimum months", tracking=True)
    min_charge = fields.Integer(string="Minimum charge", tracking=True)
    additional_month_cost = fields.Integer(string="Cost for each additional month", tracking=True)
    max_month = fields.Integer(string="Maximum month", tracking=True)
    max_charge = fields.Integer(string="Maximum charge", tracking=True)
    active = fields.Boolean(string='Active', default=True)
    
    # Multiple Policy Section
    min_months2 = fields.Integer(string="Minimum months (Multiple)", tracking=True)
    min_charge2 = fields.Integer(string="Minimum charge (Multiple)", tracking=True)
    additional_month_cost2 = fields.Integer(string="Cost for each additional month (Multiple)", tracking=True)
    max_month2 = fields.Integer(string="Maximum month (Multiple)", tracking=True)
    max_charge2 = fields.Integer(string="Maximum charge (Multiple)", tracking=True)
    
    # Employee Allowance
    emp_allowance_exit_rentry = fields.Integer(string="Emp Allowance For Exit and Reentry", tracking=True)
    
    # Loan Type
    # loan_type_id = fields.Many2one(
    #     'hr_loans.loan_advance', 
    #     string="Loan type",
    #     options="{'no_create': True}"
    # )
    
    # Request Limit
    request_limit = fields.Integer(string="Limit Company Share", tracking=True)
    
    # Statistics
    count_requests = fields.Integer(
        string="Number of requests", 
        compute="_compute_request_count",
        store=False
    )
    
    # Related Requests
    request_ids = fields.One2many(
        'hr.exit.entry.request', 
        'exit_entry_type_id', 
        string="Exit Re-entry requests",
        readonly=True
    )
    
    # Status
    state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed')
    ], string="Status", default='new', tracking=True)

    # Computed Methods
    @api.depends('request_ids')
    def _compute_request_count(self):
        for policy in self:
            policy.count_requests = len(policy.request_ids)

    # Constraints
    @api.constrains('min_months', 'max_month')
    def _check_month_validation(self):
        for policy in self:
            if policy.min_months and policy.max_month:
                if policy.min_months > policy.max_month:
                    raise ValidationError("Minimum months cannot be greater than maximum months.")
            
            if policy.min_months2 and policy.max_month2:
                if policy.min_months2 > policy.max_month2:
                    raise ValidationError("Minimum months (Multiple) cannot be greater than maximum months.")

    @api.constrains('min_charge', 'max_charge')
    def _check_charge_validation(self):
        for policy in self:
            if policy.min_charge and policy.max_charge:
                if policy.min_charge > policy.max_charge:
                    raise ValidationError("Minimum charge cannot be greater than maximum charge.")
            
            if policy.min_charge2 and policy.max_charge2:
                if policy.min_charge2 > policy.max_charge2:
                    raise ValidationError("Minimum charge (Multiple) cannot be greater than maximum charge.")

    # Action Methods
    def confirm(self):
        for policy in self:
            policy.state = 'confirmed'

    def reset(self):
        for policy in self:
            policy.state = 'new'

    def open_requests(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Exit Re-entry requests',
            'res_model': 'hr.exit.entry.request',
            'view_mode': 'tree,form',
            'domain': [('exit_entry_type_id', '=', self.id)],
            'context': {'create': False}
        }

    # Default Methods
    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('hr.exit.entry.type') or 'New'
        return super(ExitReentryPolicy, self).create(vals)