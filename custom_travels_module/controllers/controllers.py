# -*- coding: utf-8 -*-
# from odoo import http


# class CustomTravelsModule(http.Controller):
#     @http.route('/custom_travels_module/custom_travels_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_travels_module/custom_travels_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_travels_module.listing', {
#             'root': '/custom_travels_module/custom_travels_module',
#             'objects': http.request.env['custom_travels_module.custom_travels_module'].search([]),
#         })

#     @http.route('/custom_travels_module/custom_travels_module/objects/<model("custom_travels_module.custom_travels_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_travels_module.object', {
#             'object': obj
#         })
