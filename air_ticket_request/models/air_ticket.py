from odoo import models, fields, api
from odoo.exceptions import UserError

class AirTicketRequest(models.Model):
    _name = 'air.ticket.request'
    _description = 'Air Ticket Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # الحقول الأساسية
    name = fields.Char(string='Code', readonly=True, default='New')
    description = fields.Char(string='Description')
    state = fields.Selection([
        ('new', 'New'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('refused', 'Refused')
    ], string='Status', default='new', tracking=True)
    
    active = fields.Boolean(string='Active', default=True)
    
    # حقول الموظف
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, tracking=True)
    manager_id = fields.Many2one('hr.employee', string='Manager', related='employee_id.parent_id', store=True, readonly=True)
    # branch_id = fields.Many2one('hr.branch', string='Branch', related='employee_id.branch_id', store=True)
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', related='employee_id.company_id', store=True)
    job_id = fields.Many2one('hr.job', string='Job Position', related='employee_id.job_id', store=True)
    country_id = fields.Many2one('res.country', string='Nationality', store=True)

    employee_nationality = fields.Selection([
        ('native', 'Native'),
        ('Non-native', 'Non-native')
    ], string='Nationality Type')
    employee_share = fields.Float(string='Employee share')
    employee_share_method = fields.Selection([
        ('debit', 'Deduct from salary'),
        ('cash', 'Pay by cash')
    ], string='Employee share payment method')
    
    employee_eng_name = fields.Char(string='Employee arabic name', readonly=True)
    employee_identification_id = fields.Char(string='Employee Identification', readonly=True)
    employee_number = fields.Char(string='Employee Number', readonly=True)
    
    employee_address_id = fields.Many2one('res.partner', string='Work Company', readonly=True)
    employee_payroll_company_id = fields.Many2one('res.partner', string='Payroll Company', readonly=True)
    employee_sponsor_company_id = fields.Many2one('res.partner', string='Sponsor Company', readonly=True)
    
    # معلومات الهوية والجواز
    iqama_id = fields.Char(string='Iqama number', readonly=True)
    iqama_expiry_date = fields.Date(string='Iqama Expiry date', readonly=True)
    passport_no = fields.Char(string='Passport number', readonly=True)
    passport_expiry_date = fields.Date(string='Passport Expiry date', readonly=True)
    
    request_reason = fields.Selection([
        ('leave', 'Leave'),
        ('Air Ticket Cash Allowance', 'Air Ticket Cash Allowance'),
        ('Deputation / business trip', 'Deputation / business trip'),
        ('Final exit', 'Final exit'),
        ('other', 'Other')
    ], string='Air Ticket request reason')
    reason_detail = fields.Char(string='air ticket request reason')
    
    # حقول العد والإحصاء
        # حقول العد والإحصاء (غيرنا Float إلى Integer حيث مناسب)
    count_old_requests = fields.Integer(string='Number of old requests', )
    count_allocations = fields.Integer(string='Number of Allocations',)
    count_leave_requests = fields.Integer(string='Number of leave requests', )
    count_exit_rentry = fields.Integer(string='Number of Exit and Re-entry', )
    count_loan_request = fields.Integer(string='Number of loan requests', )
    # count_old_requests = fields.Integer(string='Number of old requests', compute='_compute_counts', store=False)
    # count_allocations = fields.Integer(string='Number of Allocations', compute='_compute_counts', store=False)
    # count_leave_requests = fields.Integer(string='Number of leave requests', compute='_compute_counts', store=False)
    # count_exit_rentry = fields.Integer(string='Number of Exit and Re-entry', compute='_compute_counts', store=False)
    # count_loan_request = fields.Integer(string='Number of loan requests', compute='_compute_counts', store=False)

    
    # معلومات الإجازة
    leave_request = fields.Many2one('hr.leave', string='Leave Request')
    leave_request_ids = fields.One2many('hr.leave', 'air_ticket_id', string='Leave requests')
    leave_from = fields.Datetime(string='Leave start', readonly=True)
    leave_to = fields.Datetime(string='Leave end', readonly=True)
    last_return_from_leave = fields.Date(string='Last Return From Leave', readonly=True)
    total_working_days = fields.Integer(string='Total Working Days', readonly=True)
    
    # معلومات التذكرة
    air_ticket_type = fields.Many2one('air.ticket.type', string='Air ticket type')
    travel_date = fields.Date(string='Travel date')
    expected_return_date = fields.Date(string='Expected Return date', readonly=True)
    reserve_ticket_for = fields.Selection([
        ('employee', 'Employee only'),
        ('employee_family', 'Employee and family')
    ], string='Reserve ticket for')
    
    # المعلومات المالية
    cash_allowed = fields.Selection([
        ('Yes', 'Yes'),
        ('No', 'No')
    ], string='Cash allowed')
    i_want_to = fields.Selection([
        ('cash', 'Cash'),
        ('Reserve a ticket through company', 'Reserve a ticket through company')
    ], string='I want to')
    payment_time = fields.Selection([
        ('now', 'Now'),
        ('later', 'Later')
    ], string='Payment time')
    ticket_total_price = fields.Float(string='Air ticket total price')
    company_share = fields.Float(string='Company share')
    
    # معلومات الرصيد
    show_remaining = fields.Boolean(string='Show remaining')
    current_air_ticket_balance = fields.Integer(string='Current air Ticket balance', readonly=True)
    deduct = fields.Float(string='If this Air Ticket approved, system will deduct')
    remaining_balance = fields.Float(string='Remaining Balance', readonly=True)
    ticket_allowance_per_contract = fields.Float(string='Air ticket allowance as per contract', readonly=True)
    
    # معلومات إضافية
    # contract_id = fields.Many2one('hr.contract', string='Contract', groups="hr.group_hr_user", 
    #                              domain="[('employee_id', '=', employee_id)]")  # Commented out - hr.contract not available in Odoo 19
    
    paid_through_reconciliation = fields.Boolean(string='Paid through leave reconciliation')
    payment_done = fields.Boolean(string='Payment Done', groups="account.group_account_user,account.group_account_manager")
    skip_valid_approve_req = fields.Boolean(string='Skip system Validation And approve this request', 
                                           groups="hr.group_hr_manager")
    
    # معلومات التذاكر للعائلة
    relatives_tickets = fields.Selection([
        ('Allow tickets for relatives', 'Allow tickets for relatives'),
        ('Never allow tickets for relatives', 'Never allow tickets for relatives')
    ], string='Relatives Tickets')
    number_of_relatives = fields.Float(string='Number of relatives', readonly=True)
    
    # معلومات الخروج والعودة
    can_request_exit_rentry = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='request For Exist and R-entry')
    
    air_ticket_type_can_request_exit_rentry = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Can request For Exist and R-entry')
    
    # linked_exit_rentry_id = fields.Many2one('hr.exit.entry.request', string='Linked exit Re-entry', readonly=True)  # Commented out - requires exit_reentry_request module
    # exit_rentry_ids = fields.One2many('hr.exit.entry.request', '', string='Exit and Re-entry')
    
    # الحقول المرتبطة
    # loan_request_id = fields.Many2one('loan.advance.request', string='Linked Loan request', readonly=True)
    # linked_mission_id = fields.Many2one('mowzf.mission', string='Linked Business Mission', readonly=True)
    batch_id = fields.Many2one('air.ticket.request.batch', string='Air ticket allowance Batch', readonly=True)
    
    # الحقول التقنية
    contract_leave_policy = fields.Many2one('hr.leave.type', string='Contract leave policy', readonly=True)
    air_ticket_policy = fields.Many2one('air.ticket.type', string='Annual Air Ticket Policy', readonly=True)
    contract_type_equal_leave_type = fields.Boolean(string='Contract leave policy equal leave type')
    leave_request_type_id = fields.Many2one('hr.leave.type', string='Leave request type', readonly=True)
    # loan_type_id = fields.Many2one('hr_loans.loan_advance', string='Loan type', readonly=True)  # Commented out - requires hr_loans module
    
    # حقول إضافية
    is_wait = fields.Boolean(string='wait')
    request_type = fields.Selection([
        ('Annual air ticket', 'Annual air ticket'),
        ('Other', 'Other')
    ], string='Request Type')
    
    # الحقول المرتبطة
    air_ticket_details = fields.One2many('air.ticket.details', 'request_id', string='Air Ticket Details')
    old_tickets_request_ids = fields.Many2many('air.ticket.request',
        relation='air_ticket_request_old_tickets_rel',
        column1='current_ticket_id',
        column2='old_ticket_id',
        string='Old air tickets')
    attachment_ids = fields.One2many('air.ticket.request.attachment', 'source_id', string='Attachments')
    note = fields.Html(string='Notes')
    
    # حقول المراجعة والموافقة
    request_date = fields.Date(string='Request date', default=fields.Date.today)
    reviewed_by = fields.Many2one('res.users', string='Reviewed by', readonly=True)
    reviewed_on = fields.Date(string='Reviewed On', readonly=True)
    confirmed_by = fields.Many2one('res.users', string='Confirmed by', readonly=True)
    confirmed_on = fields.Date(string='Confirmed On', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('air.ticket.request') or 'New'
        return super().create(vals)
    
    # طرق حساب الحقول
    def _compute_counts(self):
        pass
        # for record in self:
        #     # حساب عدد الطلبات القديمة
        #     record.count_old_requests = self.env['air.ticket.request'].search_count([
        #         ('employee_id', '=', record.employee_id.id),
        #         ('id', '!=', record.id),
        #         ('state', 'in', ['approved', 'reviewed'])
        #     ])
            
        #     # حساب عدد التخصيصات
        #     record.count_allocations = self.env['air.ticket.allocation'].search_count([
        #         ('employee_id', '=', record.employee_id.id)
        #     ])
            
        #     # حساب عدد طلبات الإجازة
        #     record.count_leave_requests = self.env['hr.leave'].search_count([
        #         ('employee_id', '=', record.employee_id.id),
        #         ('state', '=', 'validate')
        #     ])
            
        #     # حساب عدد طلبات الخروج والعودة
        #     record.count_exit_rentry = self.env['hr.exit.entry.request'].search_count([
        #         ('employee_id', '=', record.employee_id.id),
        #         ('state', 'in', ['approved', 'done'])
        #     ])
            
        #     # حساب عدد طلبات القروض
        #     record.count_loan_request = self.env['loan.advance.request'].search_count([
        #         ('employee_id', '=', record.employee_id.id),
        #         ('state', 'in', ['approved', 'paid'])
        #     ])
    
    # طرق الأزرار
    def review(self):
        for record in self:
            record.write({
                'state': 'reviewed',
                'reviewed_by': self.env.user.id,
                'reviewed_on': fields.Date.today()
            })
    
    def approve(self):
        for record in self:
        # التحقق إذا كان المستخدم الحالي هو مدير الموظف
            current_user_employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
            print("#########3 current_user_employee", current_user_employee)
            print("   record.manager_id.id", record.manager_id.name)
            print("   record.manager_id.parent_id id", record.employee_id.parent_id.name)
            print("   self .env.user id", self.env.user.id)
            print("   self.env.user.hasgroup('	account.group_account_manager')", self.env.user.has_group('account.group_account_manager'))
            if current_user_employee.id != record.manager_id.id and not self.env.user.has_group('account.group_account_manager'):
               raise UserError("Only the employee's manager can approve this request or the user must have the account chief group.")
            record.write({
                'state': 'approved',
                'confirmed_by': self.env.user.id,
                'confirmed_on': fields.Date.today()
            })
    
    def refuse(self):
        for record in self:
               # التحقق إذا كان المستخدم الحالي هو مدير الموظف
            current_user_employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
           
            if current_user_employee.id != record.manager_id.id and not self.env.user.has_group('account.group_account_manager'):
                 raise UserError("Only the employee's manager can approve this request or the user must have the account chief group.")
            record.state = 'refused'
    
    def reset(self):
        for record in self:
            record.state = 'new'
    
    def get_remaining(self):
        for record in self:
            # طريقة لتحديث الرصيد
            # يمكن تنفيذ العمليات الحسابية هنا
            pass
    
    def open_old_requests(self):
        pass
        self.ensure_one()
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Old Air Ticket Requests',
        #     'res_model': 'air.ticket.request',
        #     'view_mode': 'tree,form',
        #     'domain': [('employee_id', '=', self.employee_id.id), ('id', '!=', self.id)],
        #     'context': {'create': False}
        # }
    
    def open_allocations(self):
        self.ensure_one()
        pass
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Air Ticket Allocations',
        #     'res_model': 'air.ticket.allocation',
        #     'view_mode': 'tree,form',
        #     'domain': [('employee_id', '=', self.employee_id.id)],
        #     'context': {'create': False}
        # }
    
    def open_leave_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Leave Requests',
            'res_model': 'hr.leave',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.employee_id.id)],
            'context': {'create': False}
        }
    
    def open_exit_rentry_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Exit and Re-entry Requests',
            'res_model': 'hr.exit.entry.request',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.employee_id.id)],
            'context': {'create': False}
        }
    
    def open_loan_request(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Loan Requests',
            'res_model': 'loan.advance.request',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.employee_id.id)],
            'context': {'create': False}
        }

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            # تحديث معلومات الموظف تلقائياً
            self.employee_eng_name = self.employee_id.name
            self.employee_identification_id = self.employee_id.identification_id
            self.employee_number = self.employee_id.emp_no
            self.department_id = self.employee_id.department_id
            self.job_id = self.employee_id.job_id
            self.company_id = self.employee_id.company_id
            self.manager_id = self.employee_id.parent_id