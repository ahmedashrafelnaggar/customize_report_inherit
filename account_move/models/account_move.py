from odoo import fields, models


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    po_number = fields.Char(string='PO Number', attrs={'readonly': [('state', '!=', 'draft')]})

    class AccountMoveLine(models.Model):
        _inherit = 'account.move.line'
        # this field i want to add this field in add line in notebok in model account.move.line
        line_number = fields.Integer(string="Sr#", default=1)
