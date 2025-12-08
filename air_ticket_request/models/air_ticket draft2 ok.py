from odoo import models, fields, api

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
    
    active= fields.Boolean(string='Active', default=True)
    
    # branch_id = fields.Many2one('hr.branch', string='Branch', related='employee_id.branch_id', store=True)
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', related='employee_id.company_id', store=True)
    job_id = fields.Many2one('hr.job', string='Job Position', related='employee_id.job_id', store=True)
    country_id = fields.Many2one('res.country', string='Nationality', store=True)
    
    # حقول الموظف
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, tracking=True)

    employee_nationality = fields.Selection([
        ('native', 'Native'),
        ('Non-native', 'Non-native')
    ], string='Nationality Type')
    employee_share = fields.Float(string='Employee share')
    employee_share_method = fields.Selection([
        ('debit', 'Deduct from salary'),
        ('cash', 'Pay by cash')
    ], string='Employee share payment method')
    
    employee_eng_name = fields.Char(string='Employee arabic name')
    employee_identification_id = fields.Char(string='Employee Identification')
    employee_number = fields.Char(string='Employee Number')
    
    
    employee_address_id = fields.Many2one('res.partner', string='Work Company')
    employee_payroll_company_id = fields.Many2one('res.partner', string='Payroll Company')
    employee_sponsor_company_id = fields.Many2one('res.partner', string='Sponsor Company')
    
    # معلومات الهوية والجواز
    iqama_id = fields.Char(string='Iqama number', readonly=True)
    iqama_expiry_date = fields.Date(string='Iqama Expiry date', readonly=True)
    passport_no = fields.Char(string='Passport number', readonly=True)
    passport_expiry_date = fields.Date(string='Passport Expiry date', readonly=True)
    request_reason =fields.Selection([
        ('leave', 'Leave'),
        ('Air Ticket Cash Allowance', 'Air Ticket Cash Allowance'),
        ('Deputation / business trip','business_mission'),
        ('Final exit', 'Final exit'),
        ('other', 'Other')
    ])
    
    
    
    count_old_requests = fields.Integer(string='Number of loan requests')
    count_allocations = fields.Integer(string='Number of Allocations')
    count_leave_requests = fields.Float(string='Number of leave requests')
    count_exit_rentry = fields.Float(string='Number of Exit and Re-entry')
    count_loan_request = fields.Integer(string='Number of loan requests')

    # work on website
    iqama_id_ = fields.Char(string='Iqama number') 
    iqama_expiry_date_ = fields.Date(string='Iqama Expiry date') 
    passport_no_ = fields.Char(string='Passport Number') 
    passport_expiry_date_ = fields.Date(string='Passport expiry date')  

# الصحيح: يجب أن يكون حقل واحد لكل منها
    reason_detail = fields.Char(string='air ticket request reason')
    
    # معلومات الإجازة
    leave_request = fields.Many2one('hr.leave', string='Leave Request')
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
    contract_id = fields.Many2one('hr.contract', string='Contract', groups="hr.group_hr_user", domain="[('employee_id', '=', employee_id)]")
    
    paid_through_reconciliation = fields.Boolean(string='Paid through leave reconciliation')
    payment_done = fields.Boolean(string='Payment Done', groups="account.group_account_user,account.group_account_manager")
    skip_valid_approve_req = fields.Boolean(string='Skip system Validation And approve this request', groups="hr.group_hr_manager")
    
    
     # معلومات التذاكر للعائلة
    relatives_tickets = fields.Selection([
        ('Allow tickets for relatives', 'Allow tickets for relatives'),
        ('Never allow tickets for relatives', 'Never allow tickets for relatives')
    ], string='Relatives Tickets', )
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
    # linked_exit_rentry_id = fields.Many2one('hr.exit.entry.request', string='Linked exit Re-entry', readonly=True)
    
    
    # manager_id = fields.Many2one('hr.employee', string='Manager', related='employee_id.parent_id', store=True)

    # request_date = fields.Date(string='Request Date', default=fields.Date.today, required=True)
    # travel_date = fields.Date(string='Travel Date', required=True)
    
    # الحقول المرتبطة
    # loan_request_id = fields.Many2one('loan.advance.request', string='Linked Loan request', readonly=True)
    # linked_mission_id = fields.Many2one('mowzf.mission', string='Linked Business Mission', readonly=True)
    # batch_id = fields.Many2one('air.ticket.request.batch', string='Air ticket allowance Batch', readonly=True)
    
      # الحقول التقنية
    contract_leave_policy = fields.Many2one('hr.leave.type', string='Contract leave policy', readonly=True)
    air_ticket_policy = fields.Many2one('air.ticket.type', string='Annual Air Ticket Policy', readonly=True)
    contract_type_equal_leave_type = fields.Boolean(string='Contract leave policy equal leave type',)
    leave_request_type_id = fields.Many2one('hr.leave.type', string='Leave request type', readonly=True)
    # loan_type_id = fields.Many2one('hr_loans.loan_advance', string='Loan type', readonly=True)
    
    
    # حقول إضافية
    is_wait = fields.Boolean(string='wait')
    request_type = fields.Selection([
          ('Annual air ticket', 'Annual air ticket'),
        ('Other', 'Other')
    ], string='Request Type')
    
     # الحقول المرتبطة
    air_ticket_details = fields.One2many('air.ticket.details', 'request_id', string='Air Ticket Details')
     # التصحيح: تغيير تعريف حقل old_tickets_request_ids
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
        for record in self:
            # سيتم تنفيذ العمليات الحسابية هنا
            record.count_old_requests = 0
            record.count_allocations = 0
            record.count_leave_requests = 0
            record.count_exit_rentry = 0
            record.count_loan_request = 0
    
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
            record.write({
                'state': 'approved',
                'confirmed_by': self.env.user.id,
                'confirmed_on': fields.Date.today()
            })
    
    def refuse(self):
        for record in self:
            record.state = 'refused'
    
    def reset(self):
        for record in self:
            record.state = 'new'
    
    def get_remaining(self):
        # طريقة لتحديث الرصيد
        pass
    
    def open_old_requests(self):
        # طريقة لفتح الطلبات القديمة
        """
        Open old requests for the same employee.

        This method will return an action to open a tree view of all old
        requests for the same employee as the current request.
        """
        pass
    
    def open_allocations(self):
        # طريقة لفتح التخصيصات
        pass
    
    def open_leave_requests(self):
        # طريقة لفتح طلبات الإجازة
        pass
    
    def open_exit_rentry_requests(self):
        # طريقة لفتح طلبات الخروج والعودة
        pass
    
    def open_loan_request(self):
        # طريقة لفتح طلبات القروض
        pass