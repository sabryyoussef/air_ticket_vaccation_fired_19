from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ExitReentryRequest(models.Model):
    _name = "hr.exit.entry.request"
    _description = "Exit and Re-entry Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "create_date desc"

    # Basic Information
    name = fields.Char(string="Description", required=True, tracking=True)
    code = fields.Char(string="Code", readonly=True, copy=False)
    employee_id = fields.Many2one('hr.employee', string="Employee",  tracking=True)
    manager_id = fields.Many2one('hr.employee', string='Manager', related='employee_id.parent_id', store=True, readonly=True)

    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    # branch_id = fields.Many2one('hr.branch', string="Branch")
    
    # Employee Details
    employee_eng_name = fields.Char(string="Employee English Name")
    employee_identification_id = fields.Char(string="Employee Identification ID")
    employee_number = fields.Char(string="Employee Number")
    
    # Contract and Department
    # contract_id = fields.Many2one('hr.contract', string="Contract")  # Commented out - hr.contract not available in Odoo 19
    # contract_copy_id = fields.Many2one('hr.contract', string="Contract Copy")  # Commented out - hr.contract not available in Odoo 19
    department_id = fields.Many2one('hr.department', string="Department")
    department_copy_id = fields.Many2one('hr.department', string="Department Copy")
    
    # Identification Documents
    iqama_no = fields.Char(string="Iqama number")
    iqama_no_copy = fields.Char(string="Iqama number Copy")
    iqama_expiry_date = fields.Date(string="Iqama Expiry date")
    iqama_expiry_date_copy = fields.Date(string="Iqama Expiry date Copy")
    passport = fields.Char(string="Passport")
    passport_copy = fields.Char(string="Passport Copy")
    passport_expiry_date = fields.Date(string="Passport expiry date")
    passport_expiry_date_copy = fields.Date(string="Passport expiry date Copy")
    
    # Request Details
    reason = fields.Selection([
        ('vacation', 'Vacation'),
        ('emergency', 'Emergency'),
        ('business', 'Business Trip'),
        ('medical', 'Medical Treatment'),
        ('family', 'Family Visit'),
        ('air_ticket', 'Air Ticket'),
        ('other', 'Other')
    ], string="Reason", required=True, tracking=True)
    
    reason_desc = fields.Char(string="Reason description")
    exit_entry_type_id = fields.Many2one('hr.exit.entry.type', string="Exit and Re-entry Policy", required=True)
    one_mutli = fields.Selection([
        ('one_time', 'One Time'),
        ('multiple', 'Multiple')
    ], string="One time / Multiple", required=True)
    
    # Dates
    expected_travel_date = fields.Date(string="Expected travel date", required=True)
    expected_return_date = fields.Date(string="Expected return date", readonly=True)
    last_return_from_leave = fields.Date(string="Last Return From Leave")
    
    # Financial Information
    duration_in_month = fields.Integer(string="Exit and Re-entry duration in months")
    cost = fields.Float(string="Exit and Re-entry cost")
    family_cost = fields.Float(string="Family Cost")
    company_share = fields.Float(string="Company share")
    employee_share = fields.Float(string="Employee share")
    emp_benefits = fields.Float(string="Emp Benefits")
    net_emp_benefits = fields.Float(string="Net Emp Benefits", readonly=True)
    
    # Policy Details
    min_months = fields.Integer(string="Minimum months")
    min_charge = fields.Integer(string="Minimum charge")
    additional_month_cost = fields.Integer(string="Cost for each additional month")
    
    # Payment Information
    absheer = fields.Boolean(string="The employee will pay through ABSHEER")
    employee_payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('deduction', 'Salary Deduction'),
        ('company', 'Company Paid')
    ], string="Employee share payment method")
    payment_done = fields.Boolean(string="Payment Done")
    # Related Documents
    air_ticket_request_rentry_id = fields.Many2one('air.ticket.request', string="Air Ticket Request")
    leave_request_id = fields.Many2one('hr.leave', string="Leave request")
    leave_request_ids = fields.One2many('hr.leave', 'linked_exit_renry_id', string="Leave Requests")
    # leave_reconciliation_id = fields.Many2one('hr.leave.reconciliation', string="Linked Leave Reconciliation")
    # linked_loan_request_id = fields.Many2one('loan.advance.request', string="Linked Loan request")
    # loan_type_id = fields.Many2one('hr_loans.loan_advance', string="Loan type")
    
    # Statistics
    total_working_days = fields.Integer(string="Total Working Days")
    count_leave_requests = fields.Integer(string="Number of Leave requests", compute="_compute_request_counts")
    count_requests = fields.Integer(string="Number of old requests", compute="_compute_request_counts")
    limit_reached = fields.Boolean(string="Request Limit Reached")
    
    # History
    old_exit_entry_ids = fields.Many2many('hr.exit.entry.request', string="Old exit Re-entry", 
                                        compute="_compute_old_requests")
    
    # Attachments and Notes
    attachment_ids = fields.One2many('exit.entry.attachment', 'exit_entry_id', string="Attachments")
    note = fields.Html(string="Notes")
    
    # Status and Tracking
    state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('refused', 'Refused')
    ], string="Status", default='new', tracking=True)
    
    confirmed_by = fields.Many2one('res.users', string="Confirmed by", readonly=True)
    confirmed_date = fields.Date(string="Confirmed Date", readonly=True)
    active = fields.Boolean(string='Active', default=True)
    
    # Computed Methods
    @api.depends('employee_id')
    def _compute_request_counts(self):
        for record in self:
            record.count_requests = self.env['hr.exit.entry.request'].search_count([
                ('employee_id', '=', record.employee_id.id),
                ('id', '!=', record.id)
            ])
            record.count_leave_requests = self.env['hr.leave'].search_count([
                ('employee_id', '=', record.employee_id.id)
            ])
    
    @api.depends('employee_id')
    def _compute_old_requests(self):
        for record in self:
            old_requests = self.env['hr.exit.entry.request'].search([
                ('employee_id', '=', record.employee_id.id),
                ('id', '!=', record.id)
            ])
            record.old_exit_entry_ids = [(6, 0, old_requests.ids)]
    
    # Constraints
    @api.constrains('expected_travel_date', 'expected_return_date')
    def _check_dates(self):
        for record in self:
            if record.expected_travel_date and record.expected_return_date:
                if record.expected_travel_date > record.expected_return_date:
                    raise ValidationError("Expected travel date cannot be after expected return date.")
    
    # Action Methods
    def confirm(self):
        for record in self:
            current_user_employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
            print("#########3 current_user_employee", current_user_employee)
            print("   record.manager_id.id", record.manager_id.name)
            print("   record.manager_id.parent_id id", record.employee_id.parent_id.name)
            print("   self .env.user id", self.env.user.id)
            print("   self.env.user.hasgroup('	account.group_account_manager')", self.env.user.has_group('account.group_account_manager'))
            if current_user_employee.id != record.manager_id.id and not self.env.user.has_group('account.group_account_manager') and not self.env.user.has_group('hr.group_hr_manager'):
               raise UserError("Only the employee's manager can confirm this request or the user must have the account chief group or employee admin group.")
            
            record.write({
                'state': 'confirmed',
                'confirmed_by': self.env.user.id,
                'confirmed_date': fields.Date.today()
            })
    
    def refused_exit(self):
        for record in self:
            current_user_employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
            if current_user_employee.id != record.manager_id.id and not self.env.user.has_group('account.group_account_manager') and not self.env.user.has_group('hr.group_hr_manager'):
               raise UserError("Only the employee's manager can refuse this request or the user must have the account chief group or employee admin group.")
            
            record.state = 'refused'
    
    def set_to_draft(self):
        for record in self:
            record.state = 'new'
    
    def action_open_exit_re_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Exit and Reentry Renew',
            'res_model': 'hr.exit.entry.request',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_employee_id': self.employee_id.id}
        }
    
    def open_requests(self):
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Exit Re-entry requests',
            'res_model': 'hr.exit.entry.request',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.employee_id.id), ('id', '!=', self.id)],
            'context': {'create': False}
        }
    
    def open_leave_requests(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Leave requests',
            'res_model': 'hr.leave',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.employee_id.id)],
            'context': {'create': False}
        }
    
    # Default Methods
    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('hr.exit.entry.request') or 'New'
        return super(ExitReentryRequest, self).create(vals)
    
    
    
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            # تحديث معلومات الموظف تلقائياً
            self.employee_eng_name = self.employee_id.name
            self.employee_identification_id = self.employee_id.identification_id
            self.employee_number = self.employee_id.emp_no
            self.department_id = self.employee_id.department_id
            # self.job_id = self.employee_id.job_id
            self.company_id = self.employee_id.company_id
            self.manager_id = self.employee_id.parent_id