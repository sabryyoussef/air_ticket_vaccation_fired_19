{
    'name': 'Exit and Re-entry Request Management',
    'version': '19.0.1.0.0',
    'summary': 'Manage employee exit and re-entry requests with comprehensive tracking',
    'category': 'Human Resources',
    'author': 'itect',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'base', 
        'hr', 
        'mail', 
        'hr_holidays',
        'air_ticket_request'
    ],
    'data': [
        # 'security/exit_reentry_security.xml',
        'security/ir.model.access.csv',
        'data/sequence_exit_reentry_request.xml',
        'views/exit_reentry_views.xml',
        'views/exit_reentry_policy_views.xml',
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'exit_reentry_request/static/src/css/exit_reentry_styles_polices.css',
    #     ],
    # },  
     'images': ['static/description/banner.png'],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}