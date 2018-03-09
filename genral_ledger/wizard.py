# #-*- coding:utf-8 -*-
# ##############################################################################
# #
# #    OpenERP, Open Source Management Solution
# #    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
# #
# #    This program is free software: you can redistribute it and/or modify
# #    it under the terms of the GNU Affero General Public License as published by
# #    the Free Software Foundation, either version 3 of the License, or
# #    (at your option) any later version.
# #
# #    This program is distributed in the hope that it will be useful,
# #    but WITHOUT ANY WARRANTY; without even the implied warranty of
# #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# #    GNU Affero General Public License for more details.
# #
# #    You should have received a copy of the GNU Affero General Public License
# #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# #
# ##############################################################################
from odoo import models, fields, api

class GenerateGenralLedger(models.Model):
	_name = "genral.ledger"

	form = fields.Date(string="From")
	to = fields.Date(string="To")
	entry_type = fields.Selection([
		('posted', 'Actual Ledger'),
		('all', 'Virtual Ledger'),
		],default='posted',string="Target Moves")
	account = fields.Many2one('account.account',string="Account")

class BankandCash(models.Model):
	_inherit = 'account.account'

	nature = fields.Selection([
		('debit', 'Debit'),
		('credit', 'Credit'),
		])

class AccountMoveLine(models.Model):
	_inherit = 'account.move.line'

	dollar = fields.Float(string="Dollar")