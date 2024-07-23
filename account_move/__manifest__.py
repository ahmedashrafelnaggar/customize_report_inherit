# -*- coding: utf-8 -*-
{
    'name': "account_move",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_view.xml',
        'reports/account_move_report.xml',
    ],
    'assets': {
        # 'web.assets_backend': ['app_one/static/src/css/property.css'],
        # 'web.assets_backend': ['account_move/static/src/css/account_move_report.css'],
        'web.report_assets_common': ['account_move/static/src/css/account_move_report.css'],

    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
}
