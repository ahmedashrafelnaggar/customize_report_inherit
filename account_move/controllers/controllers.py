# -*- coding: utf-8 -*-
# from odoo import http


# class AccountMove(http.Controller):
#     @http.route('/account_move/account_move/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_move/account_move/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_move.listing', {
#             'root': '/account_move/account_move',
#             'objects': http.request.env['account_move.account_move'].search([]),
#         })

#     @http.route('/account_move/account_move/objects/<model("account_move.account_move"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_move.object', {
#             'object': obj
#         })
