# -*- coding: utf-8 -*-
{
	'name': "custom_travels_module",

	'summary': """
		Short (1 phrase/line) summary of the module's purpose, used as
		subtitle on modules listing or apps.openerp.com""",

	'description': """
		Long description of module's purpose
	""",

	'author': "Ebrahiem Abdellatef",
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

		'security/security.xml',
		'security/ir.model.access.csv',
		'demo/demo.xml',
		
		# Wizard
		'wizard/invoicing_report.xml',
		'wizard/travel_report.xml',
		'wizard/room_group_view.xml',
		'wizard/ticket_report.xml',
		
		#Reports
		'report/invoice_report.xml',
		'report/visa_report.xml',
		'report/pcr_report.xml',
		'report/travel_custom_view.xml',
		'report/travel_report.xml',
		'report/room_group_report.xml',
		'report/ticket_report.xml',
		'report/report.xml',
		
		'views/views.xml',
		'views/account_move.xml',
		'views/parner_view.xml',
		'views/config_view.xml',
		'views/res_user_view.xml',
		'views/res_branch_view.xml',
		
	   
	],
	'license':'LGPL-3',
	# only loaded in demonstration mode
	'demo': [
	    'demo/demo.xml',
	],
	'application': True,
	'auto_install': False,
	'license': 'LGPL-3',
}
