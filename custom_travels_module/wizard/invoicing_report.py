# -*-coding:utf-8-*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class TravelsInvoicingReport(models.TransientModel):
	_name = 'travels.invoicing.report'
	_description = 'travels invoicing Report'

	from_date = fields.Date('From Date')
	to_date = fields.Date('To Date')
	c_o = fields.Many2one('res.partner', string='C.O')
	file = fields.Binary('Download Report')
	type = fields.Selection([('invoice', 'Invoice'), ('visa', 'Visa'), ('pcr', 'PCR')], default="invoice")
	move_id = fields.Many2one('account.move', string='Invoice',
		domain="[('invoice_date', '>=', from_date),('invoice_date', '<=', to_date)]")
	branch_id = fields.Many2one("res.branch","Branch")
	branch_ids = fields.Many2many("res.branch",string="Branchs")

	def action_to_inv_report(self):
		doamin = []
		if self.c_o:
			doamin += [('c_o', '=', self.c_o.id)]
		if self.move_id:
			doamin += [('invoice_id', '=', self.move_id.id)]
		travelsobj = self.env['travels.data'].search([
				('travel_date', '>=', self.from_date),
				('travel_date', '<=', self.to_date),
				('branch_id','in',self.branch_ids.ids),
			] + doamin)
		data = {
				'travelsobj': travelsobj.ids,
				'from_date': self.from_date,
				'move_no': self.move_id.name
			}
		return self.env.ref('custom_travels_module.traveling_report_menu').report_action(None, data)

	def action_to_pcr_report(self):
		service_ids = self.env['service.service'].search([('name', 'in', ['PCR', 'pcr', 'Pcr'])])
		doamin = [('service_id', 'in', service_ids.ids)]
		if self.c_o:
			doamin += [('c_o', '=', self.c_o.id)]
		if self.move_id:
			doamin += [('invoice_id', '=', self.move_id.id)]
		travelsobj = self.env['travels.data'].search([
				('travel_date', '>=', self.from_date),
				('travel_date', '<=', self.to_date),
				('branch_id','in',self.branch_ids.ids),
			] + doamin)
		print ("travelsobj", travelsobj)
		partner_id = self.env.user.company_id.partner_id
		data = {
				'travelsobj': travelsobj.ids,
				'from_date': self.from_date,
				'move_no': self.move_id.name,
				'vat': partner_id.vat_no,
				'Tax': partner_id.vat
			}
		return self.env.ref('custom_travels_module.traveling_pcr_report_menu').report_action(None, data)

	def action_to_vis_report(self):
		if self.c_o:
			service_ids = self.env['service.service'].search([('name', 'in', ['Visa','VISA','visa','Visa Cost'])])
			travelsobj = self.env['travels.data'].search([
													('c_o', '=', self.c_o.id),
													('travel_date', '>=', self.from_date),
													('travel_date', '<=', self.to_date),
													('service_id', 'in', service_ids.ids),
													('branch_id','in',self.branch_ids.ids),
												])
			before_travelsobj = self.env['travels.data'].search([
													('c_o', '=', self.c_o.id),
													('travel_date', '<', self.from_date),
													('service_id', 'in', service_ids.ids),
													('branch_id','in',self.branch_ids.ids),
												])
			b_total = sum(before_travelsobj.mapped('sub_total'))
			payment_id = self.env['account.payment'].search([
													('partner_id', '=', self.c_o.id),
													('partner_type', '=', 'customer'),
													('date', '<', self.to_date),
												])

			move_lines = self.env['account.move.line'].search([
						('account_id', '=', self.c_o.custody_account_id.id),
						('partner_id', '=', self.c_o.id),
						('date', '>=', self.from_date),
						('date', '<=', self.to_date),
					])
			debit = sum(move_lines.mapped('debit'))
			opening_balance = sum(payment_id.mapped('amount'))
			data = {
					'travelsobj': travelsobj.ids,
					'from_date': self.from_date,
					'to_date': self.to_date,
					'debit_balance': debit,
					'opening_balance': self.c_o.currency_custody if self.c_o else 0.0,
					'b_total': b_total,
				}
			return self.env.ref('custom_travels_module.traveling_visa_report_menu').report_action(None, data)
		else:
			raise UserError(_(
						"""Please, check and select C.O for visa reports"""
					))


class TravelingInvReportMenu(models.AbstractModel):
	_name = 'report.custom_travels_module.report_world_agency'
	_description = 'report world agency Invoice'

	@api.model
	def _get_report_values(self, docids, data=None):
		# Overriding data values here since used also in _get_routes.
		docids = self.env['travels.data'].browse(data.get('travelsobj'))
		service_ids = self.env['service.service'].search([('is_default', '=', True)])
		m_total = sum(docids.filtered(lambda l:l.service_id.id in service_ids.ids).mapped('sub_total'))
		a_total = sum(docids.filtered(lambda l:l.service_id.id not in service_ids.ids).mapped('sub_total'))
		v_total = sum(docids.mapped('tax_amount'))
		partner_id = self.env.user.company_id.partner_id
		return {
			'docs': docids,
			'from_date': data.get('from_date'),
			'to_date': data.get('to_date'),
			'move_no': data.get('move_no'),
			'm_total': m_total,
			'a_total': a_total,
			'g_total': m_total + a_total,
			'v_total': v_total,
			'gr_total': m_total + a_total + v_total,
			'vat': partner_id.vat_no,
			'tax': partner_id.vat
		}

class TravelingVisaReportMenu(models.AbstractModel):
	_name = 'report.custom_travels_module.report_world_agency_visa'
	_description = 'report_world_agency_visa'

	@api.model
	def _get_report_values(self, docids, data=None):
		# Overriding data values here since used also in _get_routes.
		print ("\n\\n= = = == = = = == = = = ", data, docids)
		docids = self.env['travels.data'].browse(data.get('travelsobj'))
		return {
			'docs': docids,
			'from_date': data.get('from_date'),
			'to_date': data.get('to_date'),
		}

class TravelingPcrReportMenu(models.AbstractModel):
	_name = 'report.custom_travels_module.report_world_agency_pcr'
	_description = 'report world agency pcr'

	@api.model
	def _get_report_values(self, docids, data=None):
		# Overriding data values here since used also in _get_routes.
		docids = self.env['travels.data'].browse(data.get('travelsobj'))
		return {
			'docs': docids,
			'from_date': data.get('from_date'),
			'to_date': data.get('to_date'),
		}
