# -*- coding:utf-8 -*-

import babel
from collections import defaultdict
from datetime import date, datetime, time
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone
from pytz import utc
import calendar

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils

class HrVacationCalculation(models.Model):
    _name = 'vacation.calculation'
    _description = 'vacation calculation'
    _order = 'number'

    number = fields.Char(string='المرجع', readonly=True, copy=False, help="References",)
    employee_id = fields.Many2one('hr.employee', string='اسم الموظف', required=True, help="Employee",)
    employee_code = fields.Char(string='كود الموظف', related="employee_id.barcode", store=True) 
    ev_type = fields.Selection([
        ('vacation_settlement', 'تسويه اجازات'),
        ('service_termination', 'انهاء خدمه'),
        ('resignation', 'استقاله'),
    ], string="النوع", required=True)
    job_id = fields.Many2one('hr.job', string="المسمى الوظيفي", related='employee_id.job_id', readonly=True)
    department_id = fields.Many2one('hr.department', related='employee_id.department_id', string='القسم',
                                    readonly=True)
                                    
    joined_date = fields.Date(string="تاريخ الإنضمام", store=True,
                              help='Joining date of the employee.i.e Start date of the first contract')
    last_working_date = fields.Date(string="اخر يوم عمل",
                                          help='أخر يوم عمل مؤكد من قبل مدير الموظف',
                                          required=True)
    days_in_month = fields.Integer(
        string="عدد الأيام في الشهر",
        compute="_compute_days_in_month",
        store=True,
        help="عدد الأيام في الشهر الذي يتبع آخر يوم عمل"
    )

    legal_leave_remaining_balance = fields.Float(string="الرصيد المتبقي من الإجازة القانونية",store=True)
    total_service_days = fields.Float(string="اجمالي أيام الخدمة", default=365)
    # contract_id = fields.Many2one('hr.contract', string='العقد', required=True, help="Contract",)  # Commented out - hr.contract not available in Odoo 19
    company_id = fields.Many2one('res.company', 'الشركه', readonly=True, help="Company",
                                 default=lambda self: self.env.user.company_id,)
    currency_id = fields.Many2one(
        "res.currency",
        string="العمله",
        readonly=True,
        required=True,
        related='company_id.currency_id',
    )
    social_insurance = fields.Float(string="الضمان الاجتماعي")
    end_of_service_benefits_received = fields.Float(string="ما تم استلامه من مكافاة نهاية الخدمه")
    financial_advances_balance = fields.Float(string="سلف من الإدارة المالية")
    state = fields.Selection([('draft', 'مسوده'), ('f_approve', 'الموافقة علي الاحتساب'), ('s_approved', 'الموافقة المالية'),('post', 'الترحيل للمالية')], string='Status', default='draft')

    # Period Fields
    period_start = fields.Date(string="Period Start")
    period_end = fields.Date(string="Period End")
    
    contract_break_article_77 = fields.Float(string="كسر العقد حسب الماده 77 من مكتب العمل")
    tickets_al = fields.Float(string="بدلات تذاكر")
    
    # Notification Salary
    warning_salary_months = fields.Float(string="راتب الإنذار شهرين")

    gosi = fields.Boolean(string='هل له تأمينات؟', default=False)
    emp_gosi = fields.Monetary(string="GOSI: قيمة", help="GOSI: Saudi Employee")

    wage = fields.Monetary(string='الراتب الأساسي', store=True)  # Related to contract_id removed - hr.contract not available in Odoo 19
    hra = fields.Monetary(string='بدل السكن', help="House rent allowance.", store=True)  # Related to contract_id removed
    travel_allowance = fields.Monetary(string="بدل نقل", help="Travel allowance", store=True)  # Related to contract_id removed
    da = fields.Monetary(string="بدلات الغلاء", help="بدلات الغلاء", store=True)  # Related to contract_id removed
    meal_allowance = fields.Monetary(string="بدل طعام", help="Meal allowance", store=True)  # Related to contract_id removed
    medical_allowance = fields.Monetary(string="بدل علاج", help="Medical allowance", store=True)  # Related to contract_id removed
    other_allowance = fields.Monetary(string="بدلات أخرى", help="Other allowances", store=True)  # Related to contract_id removed

# for Alsafi
    additional_wage = fields.Float(string='المرتب الاضافي', store=True)
    # additional_wage = fields.Float(string='المرتب الاضافي', related = 'contract_id.additional_wage', store=True)
    fixed_deduction = fields.Float(string='خصومات ثابته', store=True)
    fixed_gosi = fields.Float(string='خصومات ثابته GOSI', store=True)
    # fixed_deduction = fields.Float(string='خصومات ثابته',related = 'contract_id.fixed_deduction', store=True)
    # fixed_gosi = fields.Float(string='خصومات ثابته GOSI',related = 'contract_id.fixed_gosi', store=True)
#---------------------------------------
    total = fields.Monetary(string="الاجمالي", compute= '_total_salary', store=True)

    number_of_days_lastm= fields.Integer(string='عدد أيام العمل خلال الشهر  الأخير')
    vacation_days= fields.Float(string='رصيد الاجازات المتبقية')
    vacation_days_value= fields.Float(string='قيمة رصيد الاجازات',compute='compute_all',store =True)
    totalvb = fields.Float(string="اجمالي عدد ايام العمل", store=True)
    other_al = fields.Float(string="علاوات أخرى", store=True)
    other_dd = fields.Float(string="خصومات أخرى	", store=True)
    other_absent = fields.Float(string="غيابات", store=True)
    gosi_ded = fields.Float(string="خصم ال GOSI " ,compute='compute_gosided',store=True)
    amount4lm_days = fields.Float(string="المبلغ المستحق لايام العمل خلال الشهر الأخير" ,compute='compute_all',store=True)
    amount4tvb = fields.Float(string="المبلغ المستحق لاجمالي رصيد الاجازات" ,compute='_compute_amount4tvb',store=True)
    amount_total = fields.Float(string="الإجمالي النهائي" ,compute='_compute_amount4tvb',store=True)
    end_of_service_topay = fields.Float(string="مكافئة نهاية الخدمة" ,compute='_compute_amount4tvb',store=True)
    

    note = fields.Text(string='ملاحظات')

    def calc_approve(self):
        for record in self:
            if record.state == 'draft':
                # Perform calculation logic if needed
                record.state = 'f_approve'

    def financial_approve(self):
        for record in self:
            if record.state == 'f_approve':
                # Perform financial checks or logic here
                record.state = 's_approved'

    def post_journal(self):
        for record in self:
            if record.state == 's_approved':
                # Post to journal or do accounting logic here
                record.state = 'post'

    @api.depends('last_working_date')
    def _compute_days_in_month(self):
        """
        Compute the number of days in the month for the given last_working_date.
        """
        for record in self:
            if record.last_working_date:
                # Extract year and month from the date
                date_obj = fields.Date.from_string(record.last_working_date)
                year = date_obj.year
                month = date_obj.month
                # Get the number of days in the month
                record.days_in_month = calendar.monthrange(year, month)[1]
            else:
                record.days_in_month = 30

    @api.onchange('gosi','wage','hra')
    def gosi_compute(self):
        if self.gosi : 
            self.emp_gosi = ((self.wage + self.hra )* 9.75/100)
        else: 
            self.emp_gosi = 0.00
            
    @api.depends('emp_gosi','number_of_days_lastm')
    def compute_gosided(self):
        for s in self: 
            s.gosi_ded = (s.emp_gosi/30) * s.number_of_days_lastm
            
    @api.depends('wage','hra','travel_allowance','da','meal_allowance','medical_allowance','other_allowance','additional_wage','fixed_deduction','fixed_gosi')
    def _total_salary(self):
        for s in self: 
            s.total = s.wage + s.hra + s.travel_allowance + s.da + s.meal_allowance + s.medical_allowance + s.other_allowance+ s.additional_wage- s.fixed_deduction - s.fixed_gosi
            
    @api.depends('total','number_of_days_lastm','totalvb','other_al','end_of_service_topay', 'gosi_ded', 'other_dd', 'other_absent','vacation_days' )
    def compute_all(self):
        for s in self: 
            s.amount4lm_days = (s.total/self.days_in_month) * s.number_of_days_lastm
            s.vacation_days_value = (s.vacation_days  * s.total) / 30
            
            
    @api.depends('total', 'tickets_al','totalvb', 'ev_type', 'amount4lm_days' , 'other_al' ,'end_of_service_topay' , 'contract_break_article_77', 'warning_salary_months' , 'vacation_days_value', 'gosi_ded', 'other_dd', 'social_insurance' ,'end_of_service_benefits_received' , 'financial_advances_balance','social_insurance' ,'end_of_service_benefits_received' ,'financial_advances_balance')
    def _compute_amount4tvb(self):
        for s in self:
            if s.ev_type == 'service_termination':
                if s.totalvb <= 1800:
                    s.end_of_service_topay = (s.total / 2 / 360) * s.totalvb
                elif s.totalvb > 1800:
                    s.end_of_service_topay = ((s.total / 360) * (s.totalvb - 1800)) + ((s.total / 2 / 360) * 1800)
            elif s.ev_type == 'resignation':
                if s.totalvb <= 720:
                    s.end_of_service_topay = 0.00
                elif 720 < s.totalvb <= 1800:
                    s.end_of_service_topay = ((s.total / 2 / 360) * s.totalvb) / 3
                elif 1800 < s.totalvb <= 3600:
                    s.end_of_service_topay = ((((s.total / 360) * (s.totalvb - 1800))* 2) / 3) + (((s.total / 2 / 360) * 1800)/ 3)
                elif s.totalvb > 3600:
                    s.end_of_service_topay = ((s.total / 360) * (s.totalvb - 1800)) + ((s.total / 2 / 360) * 1800)
            elif s.ev_type == 'vacation_settlement':
                s.end_of_service_topay = 0
            s.amount_total= (s.amount4lm_days + s.tickets_al + s.other_al + s.end_of_service_topay+ s.contract_break_article_77 + s.warning_salary_months+s.vacation_days_value) - (s.gosi_ded + s.other_dd+ s.other_absent + s.social_insurance + s.end_of_service_benefits_received + s.financial_advances_balance)

    @api.model
    def create(self, vals):
        company_id = vals.get('company_id') or self.env.company.id
        vals['number'] = self.env['ir.sequence'].with_company(company_id).next_by_code(
            'vacation.calculation.seq') or _('New')
        return super(HrVacationCalculation, self).create(vals)

