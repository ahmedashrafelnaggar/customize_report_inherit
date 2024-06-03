# -*-coding:utf-8-*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class TicketReport(models.TransientModel):
	_name = 'ticket.report'
	_description = 'Ticket Report'

	from_date = fields.Date('From Travel Date')
	to_date = fields.Date('To Travel Date')
	from_return_date = fields.Date('From Return Date')
	to_return_date = fields.Date('To Return Date')
	file = fields.Binary('Download Report')
	branch_id = fields.Many2one("res.branch","Branch")
	branch_ids = fields.Many2many("res.branch",string="Branchs")

	def action_print_report(self):
		travelsobj = self.env['travels.data'].search([('travel_date', '>=', self.from_date), ('return_date','<=',self.from_return_date),('branch_id','in',self.branch_ids.ids)])
		data = {
				'travelsobj': travelsobj.ids,
				'company':self.env.company.id,
			 	'from_date': self.from_date,
			}
		return self.env.ref('custom_travels_module.ticket_report_room_group').report_action(None, data)

class TicketReportMenu(models.AbstractModel):
	_name = 'report.custom_travels_module.report_ticket_template'
	_description = 'report_ticket_template'

	@api.model
	def _get_report_values(self, docids, data=None):
		docids = self.env['travels.data'].browse(data.get('travelsobj'))
		company = self.env['res.company'].browse(data.get('company'))
		shift_1_list = docids.mapped('shift_1')
		branch_list = docids.mapped('branch_id')
			
		def get_record_for_bs(branch_id,shift_1):
			travel_ids = self.env['travels.data'].search([('shift_1','=',shift_1),('branch_id','=',branch_id)])
			return travel_ids

		return {
			'docs': docids,
			'company_id':company,
			'shift_1_list':shift_1_list,
			'branch_list':branch_list,
			'get_record_for_bs':get_record_for_bs
		}