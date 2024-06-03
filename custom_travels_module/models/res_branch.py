from odoo import api, fields, models, _

class ResBranch(models.Model):
	_name = "res.branch"
	_description = "Res Branch"

	name = fields.Char('Name')

	@api.model
	def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
		if not self.env.user.has_group('custom_travels_module.group_branch_manager') and not self._context.get('see_all_branch'):
			domain = [('id','in',self.env.user.branch_ids.ids)]
			args += domain
		return super(ResBranch, self)._search(args=args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)