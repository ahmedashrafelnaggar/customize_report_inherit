# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class account_move(models.Model):
#     _name = 'account_move.account_move'
#     _description = 'account_move.account_move'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
