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
    _name = 'report.membership_reports.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('membership_reports.customer_report')
        active_wizard = self.env['membership.reports'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['membership.reports'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['membership.reports'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        date = record_wizard.date
        branch = record_wizard.branch
        types = record_wizard.types
        record = self.env['reg.form'].search([('branch','=',record_wizard.branch.id)])

        if types == 'active':
            membership = []
            for x in record:
                if x.stages == 'member':
                    membership.append(x)

        if types == 'nonactive':
            membership = []
            for x in record:
                if x.stages == 'non_member':
                    membership.append(x)

        if types == 'discontinue':
            current_month = str(date[:7])
            membership = []
            for x in record:
                if x.stages == 'non_member':
                    if str(x.write_date[:7]) == current_month:
                        membership.append(x)


        if types == 'new':
            current_month = str(date[:7])
            membership = []
            for x in record:
                if x.stages == 'member':
                    if x.joining:
                        if str(x.joining[:7]) == current_month:
                            membership.append(x)


        if types == 'diet':
            membership = []
            for x in record:
                if x.stages == 'member':
                    if x.diet_plan == True:
                        membership.append(x)


        if types == 'health':
            membership = []
            for x in record:
                if x.stages == 'member':
                    if x.health == True:
                        membership.append(x)




        

        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'reg.form',
            'membership': membership,
    
            }

        return report_obj.render('membership_reports.customer_report', docargs)