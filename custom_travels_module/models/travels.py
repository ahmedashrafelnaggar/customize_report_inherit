from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date

class TravelsData(models.Model):
	_name = 'travels.data'
	_description = 'Travels Data'
	_rec_name = 'ticket_number'

	travel_type = fields.Selection([
		('arr', 'ARR'),
		('dep', 'DEP'),

	], default='arr', string='ARR or DEP')

	vessel_id = fields.Char(string="Vessel Name")
	vessel_name = fields.Char(string='Name Of Person')
	companion_name = fields.Char(string='Name Of Company')
	vessel_nationality = fields.Many2one('res.country', string='Nationality')
	travellers_number = fields.Integer(string='Travellers Number', default=1)
	travel_date = fields.Date(string='Travel Date')
	return_date = fields.Date(string='Return Date')
	service_id = fields.Many2one('service.service', 'Service Name')
	flight_no = fields.Char(string='Flight Number')
	flight_time_format = fields.Float(string='Flight Time')
	#destination = fields.Char(string='Destination')
	destination = fields.Many2one('res.country.state', string='Destination')
	pcr = fields.Integer(string='Quantity', default=1)
	price = fields.Float('Price')
	sub_total = fields.Float('Sub Total', compute="compute_amount")
	c_o = fields.Many2one('res.partner', string='C.O',default=lambda self:self.env.user.partner_id.id)
	shift_1 = fields.Many2one('travels.shift', string='Trip Type')
	shift_2 = fields.Many2one('travels.shift', string='Shift 2')
	shift_3 = fields.Many2one('travels.shift', string='Office')
	state = fields.Selection([('draft', 'Draft'),
						   ('approve', 'Approved'),
						   ('confirm', 'Confirm'),
						   ('invoice', 'Invoiced')],
						  default='draft', string='Status')
	hjrj_y_from = fields.Selection([('1445', '1445'),
									('1446', '1446'),
									('1447', '1447'),
									('1448', '1448'),
									('1449', '1449'),
							  ],
							 default='1445', string='Hijri Year From')
	hjrj_m_from = fields.Selection([('1', '1'),
							  ('2', '2'),
							  ('3', '3'),
							  ('4', '4'),
									('5', '5'),
									('6', '6'),
									('7', '7'),
									('8', '8'),
									('9', '9'),
									('10', '10'),
									('11', '11'),
							  ('12', '12')],
							 default='1', string='Hijri Month From')
	hjrj_d_from = fields.Selection([('1', '1'),
							  ('2', '2'),
							  ('3', '3'),
							  ('4', '4'),
									('5', '5'),
									('6', '6'),
									('7', '7'),
									('8', '8'),
									('9', '9'),
									('10', '10'),
									('12', '12'),
									('13', '13'),
									('14', '14'),
									('15', '15'),
									('16', '16'),
									('17', '17'),
									('18', '18'),
									('19', '19'),
									('20', '20'),
									('21', '21'),
									('22', '22'),
									('23', '23'),
									('24', '24'),
									('25', '25'),
									('26', '26'),
									('27', '27'),
									('28', '28'),
									('29', '29'),
									('30', '30')],
							 default='1', string='Hijri Day From')

	hjrj_y_to = fields.Selection([('1445', '1445'),
									('1446', '1446'),
									('1447', '1447'),
									('1448', '1448'),
									('1449', '1449'),
									],
								   default='1445', string='Hijri Year To')
	hjrj_m_to = fields.Selection([('1', '1'),
									('2', '2'),
									('3', '3'),
									('4', '4'),
									('5', '5'),
									('6', '6'),
									('7', '7'),
									('8', '8'),
									('9', '9'),
									('10', '10'),
									('11', '11'),
									('12', '12')],
								   default='1', string='Hijri Month To')
	hjrj_d_to = fields.Selection([('1', '1'),
									('2', '2'),
									('3', '3'),
									('4', '4'),
									('5', '5'),
									('6', '6'),
									('7', '7'),
									('8', '8'),
									('9', '9'),
									('10', '10'),
									('12', '12'),
									('13', '13'),
									('14', '14'),
									('15', '15'),
									('16', '16'),
									('17', '17'),
									('18', '18'),
									('19', '19'),
									('20', '20'),
									('21', '21'),
									('22', '22'),
									('23', '23'),
									('24', '24'),
									('25', '25'),
									('26', '26'),
									('27', '27'),
									('28', '28'),
									('29', '29'),
									('30', '30')],
								   default='1', string='Hijri Day To')

	invoice_id = fields.Many2one('account.move', string='Invoice')
	tax_id = fields.Many2one('account.tax', 'Taxes')
	tax_amount = fields.Float('Tax Total', compute="compute_amount")
	amount_total = fields.Float('Amount Total', compute="compute_amount")
	notes = fields.Char("Notes")
	branch_id = fields.Many2one("res.branch","Branch",default=lambda self:self.env.user.branch_id)
	ticket_number = fields.Char("Ticket Number")
	ticket_date = fields.Char("Ticket Date",default=date.today())
	mobile_no = fields.Char("Mobile No")
	customer_id = fields.Char("Customer ID")
	room_type_id = fields.Many2one("room.type","Room Type")
	einv_sa_qr_code_str = fields.Char(related="invoice_id.einv_sa_qr_code_str")
	travel_date_hijri_str = fields.Char('Travel Date Hijri',compute="compute_travel_date")
	return_date_hijri_str = fields.Char('Return Date Hijri',compute="compute_return_date")
	is_branch_manager = fields.Boolean("Is Branch Manager",compute="compute_on_group_branch_manager")

	def compute_on_group_branch_manager(self):
		for rec in self:
			if self.env.user.has_group("custom_travels_module.group_branch_manager"):
				rec.is_branch_manager = True
			else:
				rec.is_branch_manager = False

	@api.depends('travel_date')
	def compute_travel_date(self):
		for rec in self:
			if rec.travel_date:
				rec.with_context(
					{'field_to': 'travel_date_hijri_str', 'field_from': 'travel_date'}).Gregorian2hijri()
			else:
				rec.travel_date_hijri_str = ""

	@api.depends('return_date')
	def compute_return_date(self):
		for rec in self:
			if rec.return_date:
				rec.with_context(
					{'field_to': 'return_date_hijri_str', 'field_from': 'return_date'}).Gregorian2hijri()
			else:
				rec.return_date_hijri_str = ""

	@api.model
	def default_get(self, fields_list):
		result = super(TravelsData, self).default_get(fields_list)
		default_service = self.env['service.service'].search([('is_default','=',True)],limit=1)
		result.update({
			'service_id': default_service.id if default_service else False,
			'is_branch_manager': True if self.env.user.has_group("custom_travels_module.group_branch_manager") else False,
		})
		return result

	def compute_amount(self):
		for rec in self:
			rec.sub_total = rec.pcr * rec.price
			amount_tax = rec.sub_total * rec.tax_id.amount / 100 if rec.tax_id else 0.0
			rec.tax_amount = amount_tax
			rec.amount_total = amount_tax + rec.sub_total

	@api.onchange('c_o','c_o.price_categories_line','vessel_nationality','travellers_number','travel_type','service_id')
	def onchange_on_price(self):
		for rec in self:
			if rec.vessel_nationality and rec.c_o:
				service_line = rec.c_o.price_categories_line.filtered(lambda line:rec.service_id == line.service_id and rec.travel_type == line.travel_type)
				if service_line:
					special_line = service_line.filtered(lambda line:rec.vessel_nationality.id in line.country_ids.ids and line.active_inactive) 
					standard_line = service_line.filtered(lambda line:rec.travellers_number <= line.number)
					if special_line and special_line.special_price:
						rec.price = special_line[0].special_price
					else:
						rec.price = standard_line[0].price if standard_line else 0
				else:
					rec.price = 0.0
			else:
				rec.price = 0.0

	@api.onchange('travellers_number')
	def onchange_on_quantity(self):
		for rec in self:
			rec.pcr = rec.travellers_number

	# Confirm Travels
	def confirm_action(self):
		# done_lines = self.filtered(lambda x:x.state not in ('approve'))
		# if done_lines:
		# 	raise ValidationError(_("""Please, check some Travellers are draft and invoiced."""))
		# else:
		for rec in self:
			rec.state = 'confirm'

	# Approved Travels
	def approve_action(self):
		# done_lines = self.filtered(lambda x:x.state not in ('draft'))
		# if done_lines:
		# 	raise ValidationError(_("""Please, check some Travellers are confirmed and invoiced."""))
		# else:
		for rec in self:
			rec.state = 'approve'

	# Reset Darft
	def reset_to_draft_action(self):
		for rec in self:
			rec.state = 'draft'

	def action_duplicate(self):
		for record in self:
			record.copy()
	
	# Create Invoices
	def action_create_invoice(self):
		# draft =  self.filtered(lambda x:x.state == 'draft')
		# if draft:
		# 	raise ValidationError(
		# 						_(
		# 							"""Please, check some Travellers are not confirmed. without confirmation we can't do invoiced!!!"""
		# 						))

		# records =  self.filtered(lambda x:x.state == 'confirm')
		# records = self.filtered(invoice_id == False)])
		records_1 = self.filtered(lambda x:not x.invoice_id)
		if records_1:
			co_list = set(records_1.mapped('c_o').ids)
			if len(co_list) == 1:
				lines = []
				service_list = records_1.mapped('service_id').ids
				records = self.search([('ticket_number','=',records_1[0].ticket_number)])
				for record in records:
				# for service in service_list:
					service = record.service_id.id
					line_list = record.filtered(lambda x:x.service_id.id == service)
					if line_list:
						tax_line_list = line_list.filtered(lambda x:x.tax_id)
						untax_line_list = line_list.filtered(lambda x:not x.tax_id)
						if tax_line_list:
							tax_list = tax_line_list.mapped('tax_id').ids
							for tax in tax_list:
								tax_line = tax_line_list.filtered(lambda x:x.tax_id.id == tax)
								price_categories_line = tax_line[0].c_o.price_categories_line.filtered(lambda x:x.service_id == tax_line[0].service_id and x.travel_type == tax_line[0].travel_type)
								if price_categories_line:
									tax_price = sum(tax_line.mapped('price'))
									tax_pcr = sum(tax_line.mapped('pcr'))
									vals_line = {
										'name':price_categories_line.service_id.name,
										'account_id':price_categories_line.account_id.id,
										# 'analytic_account_id':price_categories_line.analytic_account_id.id,
										'quantity':tax_pcr,
										'price_unit':tax_price / tax_pcr if tax_pcr else 0,
										'tax_ids':[(6,0,tax_line[0].tax_id.ids)]
									}
									lines.append([0,0,vals_line])
								else:
									raise ValidationError(
											_(
												"""Please, check this service for customer. because of in we haven't find out. ' {name} ' """.format(name=self.service_id.name)
											))
						if untax_line_list:
							price_categories_line = untax_line_list[0].c_o.price_categories_line.filtered(lambda x:x.service_id == untax_line_list[0].service_id and x.travel_type == untax_line_list[0].travel_type)
							if price_categories_line:
								vals_line = {
									'name':price_categories_line.service_id.name,
									'account_id':price_categories_line.account_id.id,
									# 'analytic_account_id':price_categories_line.analytic_account_id.id,
									'quantity':sum(untax_line_list.mapped('pcr')),
									'price_unit':sum(untax_line_list.mapped('price')) / sum(untax_line_list.mapped('pcr')),
								}
								lines.append([0,0,vals_line])
							else:
								raise ValidationError(
										_(
											"""Please, check this service for customer. because of in we haven't find out. ' {name} ' """.format(name=rec.service_id.name)
										))

				# for rec in self:
				# 	price_categories_line = rec.c_o.price_categories_line.filtered(lambda x:x.service_id == rec.service_id and x.travel_type == rec.travel_type)
				# 	if price_categories_line:
				# 		vals_line = {
				# 			'name':price_categories_line.service_id.name,
				# 			'account_id':price_categories_line.account_id.id,
				# 			'analytic_account_id':price_categories_line.analytic_account_id.id,
				# 			'quantity':rec.pcr or 1,
				# 			'price_unit':rec.price
				# 		}
				# 		lines.append((0,0,vals_line))
				# 	else:
				# 		raise ValidationError(
				# 				_(
				# 					"""Please, check this service for customer. because of in we haven't find out. ' {name} ' """.format(name=rec.service_id.name)
				# 				))
				if lines:
					vals = {'partner_id':records_1[0].c_o.id,'travellers':True,'move_type':'out_invoice','invoice_line_ids':lines}
					invoice_id = self.env['account.move'].create(vals)
					records_1.invoice_id = invoice_id.id
					records_1.state = 'invoice'
			else:
				raise ValidationError(
								_(
									"""Found Multiple Co. Please check only similar. Co we can do invoice."""
								))
		else:
			raise ValidationError(
								_(
									"""All Travellers are already invoiced. Thank you!!!"""
								))

	@api.constrains('pcr','travel_type')
	def warning_pcr(self):
		for record in self:
			service_line = record.c_o.price_categories_line.filtered(lambda line:record.service_id == line.service_id and record.travel_type == line.travel_type)
			if service_line:
				if not(service_line[0].greater_than_number <= record.pcr <= service_line[0].number):
					raise ValidationError(_("Sorry !! You have to enter quantity from {} to {}.".format(service_line[0].greater_than_number,service_line[0].number)))


	def open_travel_invoice(self):
		self.ensure_one()
		return {
			'name': 'Invoices',
			'view_id': False,
			'view_mode': 'form',
			'res_model': 'account.move',
			'type': 'ir.actions.act_window',
			'res_id':self.invoice_id.id,
		}

	@api.model
	def create(self, vals):
		vals['ticket_number'] = self.env['ir.sequence'].next_by_code('travels.data') or '/'
		res = super(TravelsData, self).create(vals)
		return res

	def copy(self):
		seq_record = self.env.ref("custom_travels_module.seq_travels_data")
		old_next_number = seq_record.number_next_actual
		res = super().copy()
		res.ticket_number = self.ticket_number
		seq_record.number_next_actual = old_next_number
		return res

class TravellersShift(models.Model):
	_name = 'travels.shift'
	_description = 'Travels Shift'
	_rec_name = 'name'

	name = fields.Char('Name')
	partner_id = fields.Many2one('res.partner')

# class TravellersNationality(models.Model):
# 	_name = 'travels.nationality'
# 	_description = 'Travels Nationality'
# 	_rec_name = 'name'

# 	name = fields.Char('Name')