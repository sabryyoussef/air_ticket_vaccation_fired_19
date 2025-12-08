from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResCountryInherit(models.Model):
    _inherit = 'res.country'

    arabic_name = fields.Char(string='Country Arabic Name')
    check_iqama_expiry = fields.Boolean(string='Check for IQAMA / National ID expiry')
    check_passport_expiry = fields.Boolean(string='Check for Passport expiry date')
    company_amount = fields.Float(string='Company amount')
    company_share = fields.Float(string='Company share')
    # contract_id = fields.Many2one('hr.contract', string='Contract')  # Commented out - hr.contract not available in Odoo 19
    count_employees = fields.Integer(string='Number Of Employees')
    employee_amount = fields.Float(string='Employee amount')
    employee_ids = fields.One2many('hr.employee', 'country_id', string='Employees')
    employee_share = fields.Float(string='Employee share')
    eos_notice_period = fields.Integer(string='EOS Notice period')
    gosi_calc_based_on = fields.Selection([
        ('basic', 'Basic Salary'),
        ('gross', 'Gross Salary'),
        ('fixed', 'Fixed Amount')
    ], string='Gosi Calculation based on')
    gosi_for_this = fields.Selection([
        ('required', 'Required'),
        ('not_required', 'Not Required'),
        ('optional', 'Optional')
    ], string='GOSI for this nationality')
    is_saudi = fields.Boolean(string='Native')
    manual_gosi_salary = fields.Float(string='Manual Gosi Salary')
    max_gosi_amount = fields.Integer(string='Maximum Gosi amount')
    minimum_gosi_salary = fields.Float(string='Minimum Gosi Salary')
    note = fields.Html(string='Notes')
    one_way_price = fields.Float(string='One way price')
    renew_before_contract = fields.Integer(string='Start contract Renewing Process Before Contract End Date')
    return_price = fields.Float(string='Return price')
    salary_for_gosi = fields.Float(string='Salary for GOSI')
    start_gosi_payslip_date = fields.Date(string='Start include GOSI in Payslip from')
    who_will_pay = fields.Selection([
        ('company', 'Company'),
        ('employee', 'Employee'),
        ('both', 'Both Company and Employee')
    ], string='Who will pay the GOSI')