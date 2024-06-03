# -*-coding:utf-8-*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class TravelsReport(models.TransientModel):
	_name = 'travels.report'
	_description = 'travels report'

	from_date = fields.Date('From Travel Date')
	to_date = fields.Date('To Travel Date')
	from_return_date = fields.Date('From Return Date')
	to_return_date = fields.Date('To Return Date')
	filter_by = fields.Selection([('vessel_name','Vessel Name'),('tickit_no','Ticket No')],default="vessel_name",string="Group By")
	file = fields.Binary('Download Report')
	branch_id = fields.Many2one("res.branch","Branch")
	branch_ids = fields.Many2many("res.branch",string="Branchs")

	def action_print_report(self):
		travelsobj = self.env['travels.data'].search([('travel_date', '>=', self.from_date), ('return_date','<=',self.from_return_date),('branch_id','in',self.branch_ids.ids)])
		if self.filter_by == 'vessel_name':
			travelsobj = self.env['travels.data'].search([('travel_date', '>=', self.from_date), ('return_date','<=',self.from_return_date),('branch_id','in',self.branch_ids.ids)],order='vessel_id asc')
		data = {
				'travelsobj': travelsobj.ids,
				'company':self.env.company.id,
			 	'from_date': self.from_date,
			}
		return self.env.ref('custom_travels_module.traveling_custom_report_menu').report_action(None, data)

class TravelingReportMenu(models.AbstractModel):
	_name = 'report.custom_travels_module.report_travel'
	_description = 'report_travel'

	@api.model
	def _get_report_values(self, docids, data=None):
		# Overriding data values here since used also in _get_routes.
		docids = self.env['travels.data'].browse(data.get('travelsobj'))
		company = self.env['res.company'].browse(data.get('company'))
		return {
			'docs': docids,
			'company_id':company,
		}