from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class ServiceService(models.Model):
	_name = "service.service"
	_description = "Service Service"
	_order = "name asc"

	name = fields.Char('Name')
	partner_id = fields.Many2one('res.partner','Partner')
	is_default = fields.Boolean('Is Default')
	
	@api.constrains('name')
	def check_name(self):
		for rec in self:
			same_service = self.env['service.service'].search([('name','=',rec.name),('id','!=',rec.id)])
			if same_service:
				raise UserError(_("This Name is already exist !!!"))

class RoomType(models.Model):
	_name = "room.type"
	_description = "Room Type"
	_order = "name asc"

	name = fields.Char('Name')
	
	@api.constrains('name')
	def check_name(self):
		for rec in self:
			same_service = self.env['room.type'].search([('name','=',rec.name),('id','!=',rec.id)])
			if same_service:
				raise UserError(_("This Name is already exist !!!"))

