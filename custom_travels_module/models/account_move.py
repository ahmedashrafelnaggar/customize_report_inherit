from odoo import api, fields, models, _
import base64
from datetime import datetime
import qrcode

class AccountMoveInherit(models.Model):
	_inherit = 'account.move'

	travels_id = fields.Many2one('travels.data', string='Travellers Data')
	shift_to_hotel = fields.Integer(string='Shift To Hotel')
	shift_to_port = fields.Integer(string='Shift To Port')

	travellers = fields.Boolean('Travellers')
	einv_sa_qr_code_str = fields.Char(string='QR Code', compute='_compute_eniv_qr_code_str')

	@api.depends('amount_total', 'amount_untaxed', 'company_id', 'company_id.vat')
	def _compute_eniv_qr_code_str(self):
		""" Generate the qr code for Saudi e-invoicing. Specs are available at the following link at page 23
		https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20210528_ZATCA_Electronic_Invoice_Security_Features_Implementation_Standards_vShared.pdf
		https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/QRCodeCreation.pdf
		"""

		def get_qr_encoding(tag, field):
			company_name_byte_array = field.encode('UTF-8')
			company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
			company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
			return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

		for record in self:
			qr_code_str = ''
			seller_name_enc = get_qr_encoding(1, record.company_id.display_name)
			company_vat_enc = get_qr_encoding(2, record.company_id.vat if record.company_id.vat else '')
			time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'), datetime.now())
			timestamp_enc = get_qr_encoding(3, time_sa.isoformat())
			invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
			total_vat_enc = get_qr_encoding(5, str(record.currency_id.round(
				record.amount_total - record.amount_untaxed)))

			str_to_encode = seller_name_enc + company_vat_enc + timestamp_enc + invoice_total_enc + total_vat_enc
			qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')
			record.einv_sa_qr_code_str = qr_code_str