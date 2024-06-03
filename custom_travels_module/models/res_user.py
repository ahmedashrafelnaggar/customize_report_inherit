from odoo import api, fields, models, _

class ResUsers(models.Model):
	_inherit = "res.users"

	branch_ids = fields.Many2many("res.branch",string="Branchs")
	branch_id = fields.Many2one("res.branch","Branch",domain="[('id','in',branch_ids)]")