from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
	_inherit = 'res.partner'

	# nationality = fields.Many2one('travels.nationality', string='Nationality')
	price_categories_line = fields.One2many('price.categories', 'partner_id', 'Price Categories')
	custody_account_id = fields.Many2one('account.account', 'Custody Account Name')
	currency_custody = fields.Float('Currency Custody', compute="_compute_price")
	vat_no = fields.Char('VAT No.')

	def _compute_price(self):
		for rec in self:
			if rec.custody_account_id:
				move_lines = self.env['account.move.line'].search([
						('account_id', '=', rec.custody_account_id.id),
						('partner_id', '=', rec.id)
					])
				pay_move_lines = self.env['account.move.line'].search([
						('account_id', '=', rec.property_account_receivable_id.id),
						('partner_id', '=', rec.id)
					])
				debit = sum(move_lines.mapped('debit'))
				credit = sum(move_lines.mapped('credit'))
				rec.currency_custody = debit - credit
			else:
				rec.currency_custody = 0.0



class PriceCategories(models.Model):
	_name = "price.categories"
	_description = "Price Categories"
	_rec_name = "service_id"

	partner_id = fields.Many2one('res.partner','Partner')
	categ_no = fields.Integer('Categ. No.', compute="compute_on_categ_no")
	service_id = fields.Many2one('service.service','Service Name')
	travel_type = fields.Selection([('arr', 'ARR'),('dep', 'DEP')], default='arr', string='ARR or DEP')
	greater_than_number = fields.Integer('Greater Than')
	number = fields.Integer('Less Than')
	price = fields.Float('Standard Price')
	country_ids = fields.Many2many('res.country','rel_res_partner_country_id','partner_id','country_id','Special Nationalities')
	special_price = fields.Float('Special Price')
	active_inactive = fields.Boolean('Active/Inactive')
	account_id = fields.Many2one('account.account','Account Name')
	analytic_account_id = fields.Many2one('account.analytic.account','Analytic Account')

	def compute_on_categ_no(self):
		for rec in self:
			price_categories_line = rec.partner_id.price_categories_line
			max_number = max(price_categories_line.mapped('categ_no'))
			rec.categ_no = max_number + 1

	@api.constrains('service_id','travel_type','country_ids','active_inactive')
	def warning_price_categories(self):
		for record in self:
			price_categorie_line = self.search([('id','!=',record.id),('service_id','=',record.service_id.id),('travel_type','=',record.travel_type),('country_ids','in',record.country_ids.ids),('active_inactive','=',record.active_inactive)],limit=1)
			if price_categorie_line:
				raise ValidationError(_("Sorry !! You can't not create same line.\n Please check your all line."))
