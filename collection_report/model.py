#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################
from openerp import models, fields, api
from datetime import timedelta,datetime,date
from dateutil.relativedelta import relativedelta
import time

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.collection_report.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('collection_report.customer_report')
        active_wizard = self.env['payment.reports'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['payment.reports'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['payment.reports'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        date_from = record_wizard.date_from
        date_to = record_wizard.date_to
        branch = record_wizard.branch
        journal_id = record_wizard.journal_id
        b_types = record_wizard.b_types


        if b_types == "all":
            branches = []
            rec = self.env['res.users'].search([])
            for x in rec:
                branches.append(x.branch)

        if b_types == "specfic":
            branches = []
            for x in branch:
                branches.append(x)


        records = []
        def get_record(attr):
            del records[:]
            rec = self.env['customer.payment.bcube'].search([('branch','=',attr),('journal_id','=',record_wizard.journal_id.id),('date','>=',record_wizard.date_from),('date','<=',record_wizard.date_to)])
            print rec
            print "nnnnnnnnnnnnnnnnnnnnnnnnn"
            for x in rec:
                records.append(x)
            print records
            print "nnnnnnnnnnnnnnnnn"
            print "nnnnnnnnnnnnnnnnn"


        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'date_from': date_from,
            'date_to': date_to,
            'branch': branch.name,
            'journal_id': journal_id.name,
            'records': records,
            'branches': branches,
            'get_record': get_record,
    
            }

        return report_obj.render('collection_report.customer_report', docargs)