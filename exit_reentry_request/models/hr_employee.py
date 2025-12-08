from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    # Nationality settings
    nationality_typ = fields.Selection([
        ('Native', 'Native'),
        ('Non-native', 'Non-native'),
        ('All Nationalities', 'All Nationalities')
    ], string='نوع الجنسية', tracking=True)