# -*- coding: utf-8 -*-

{
    'name': 'End Service / Vacation calculation',
    'category': 'Generic Modules/Human Resources',
    'version': '19.0.1.0.0',
    'author': 'Odoo SA,iTech',
    'company': 'iTech',
    'maintainer': 'iTech',
    'website': 'https://www.iTech.com.eg',
    'summary': 'Manage your End service & vacation calculation',
    'images': ['static/description/banner.png'],
    'description': "vacation calculation",
    'depends': [
        'base',
        'hr',
        'project',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/user_groups.xml',
        'report/tvc_reports.xml',
        'report/tvc_report_templates.xml',
        'report/employee_settlement_report_template.xml',
        'views/vacation_calculation_views.xml',
        'data/hr_vacation_calculation_sequence.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
