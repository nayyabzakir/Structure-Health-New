#-*- coding:utf-8 -*-
from datetime import datetime, timedelta , date
from dateutil.relativedelta import relativedelta
import time
from odoo import models, fields, api


class MyDash(models.Model):
    _name = 'my.dash'
    _rec_name = 'name'
    _description = 'New Description'

    current_member_count = fields.Integer(string="Current Members", compute='count_current_members')
    cancel_member_count = fields.Integer(string="Cancel Members", compute='count_cancel_members')
    new_member_count = fields.Integer(string="Cancel Members", compute='new_cancel_members')
    cancel_massage_count = fields.Integer(string="Cancel Massage", compute='count_cancel_massage')
    booked_massage_count = fields.Integer(string="Cancel Massage", compute='count_booked_massage')
    daily_visitor_count = fields.Integer(string="Daily Visitor", compute='count_daily_visitor')
    monthly_visitor_count = fields.Integer(string="Daily Visitor", compute='count_monthly_visitor')
    daily_receipts_amount = fields.Integer(string="Daily Receipts Amount", compute='_daily_receipts_amount')
    monthly_receipts_amount = fields.Integer(string="Monthly Receipts Amount", compute='_monthly_receipts_amount')
    name = fields.Char()

    def create_my_dash(self):
        record = self.env['my.dash'].create({
            'name':"My DashBoard"
        })


    @api.one
    def count_current_members(self):
        self.current_member_count = self.env['reg.form'].search_count([('stages', '=', 'member')])

    @api.one
    def count_cancel_members(self):
        self.cancel_member_count = self.env['reg.form'].search_count([('stages', '=', 'cancel')])

    @api.one
    def new_cancel_members(self):
        current_month = str(date.today())
        rec = self.env['reg.form'].search([('stages', '=', 'member')])
        count = 0
        for x in rec:
            if x.joining:
                if str(x.joining[:7]) == str(current_month[:7]):
                    count = count + 1
        self.new_member_count = count


    @api.one
    def count_cancel_massage(self):
        self.cancel_massage_count = self.env['struct.appointment'].search_count([('stages', '=', 'cancel')])

    @api.one
    def count_booked_massage(self):
        self.booked_massage_count = self.env['struct.appointment'].search_count([('stages', '=', 'booked')])

    @api.one
    def count_daily_visitor(self):
        self.daily_visitor_count = self.env['struct.visitor'].search_count([('date','=',date.today())])

    @api.one
    def count_monthly_visitor(self):
        current_month = str(date.today())
        rec = self.env['struct.visitor'].search([])
        count = 0
        for x in rec:
            if x.date:
                if str(x.date[:7]) == str(current_month[:7]):
                    count = count + 1
        self.monthly_visitor_count = count

    @api.one
    def _daily_receipts_amount(self):
        rec = self.env['customer.payment.bcube'].search([('date', '=', date.today()),('receipts', '=',True)])
        for x in rec:
            self.daily_receipts_amount = self.daily_receipts_amount + x.amount

    @api.one
    def _monthly_receipts_amount(self):
        current_month = str(date.today())
        rec = self.env['customer.payment.bcube'].search([('receipts', '=', True)])
        for x in rec:
            if str(x.date[:7]) == str(current_month[:7]):
                self.monthly_receipts_amount = self.monthly_receipts_amount + x.amount