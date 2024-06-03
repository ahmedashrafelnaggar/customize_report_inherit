# -*- coding: utf-8 -*-

from odoo import api, models, api, _
from datetime import datetime

class ReportTravelTemplate(models.AbstractModel):
	_name = 'report.custom_travels_module.report_travel_template'

	def _get_report_values(self, docids, data=None):
		docs = self.env['travels.data'].browse(docids)
		tickiet_name_list = set(docs.mapped('ticket_number'))
		
		def get_record_from_number(tickiet_no):
			travel_id = self.env['travels.data'].search([('ticket_number','=',tickiet_no),('id','in',docs.ids)],limit=1)
			return travel_id

		def get_line_from_number(tickiet_no):
			travel_ids = self.env['travels.data'].search([('ticket_number','=',tickiet_no)])
			return travel_ids

		return {
			'docs': docs,
			'tickiet_name_list':tickiet_name_list,
			'get_record_from_number':get_record_from_number,
			'get_line_from_number':get_line_from_number,
		}