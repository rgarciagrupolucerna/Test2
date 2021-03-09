# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PolizaXLS(models.TransientModel):
    _name = "poliza.xls"
    _description = 'Poliza XLS'
    
    todos = fields.Boolean(string="Todos")
    rango_de_empleados1 = fields.Integer(string='Rango de empleados')
    rango_de_empleados2 = fields.Integer(string="TO")
    payslip_batch_id = fields.Many2one('hr.payslip.run','Payslip Run')
    
    def export_report_xlsx(self):
        #if not self.todos and self.rango_de_empleados1 and self.rango_de_empleados2:
        start = self.rango_de_empleados1
        end = self.rango_de_empleados2 
        todos = self.todos
        if todos:
            return self.payslip_batch_id.with_context(start_range=start,end_range=end).poliza_export_report_xlsx()
        else:
            return self.payslip_batch_id.poliza_export_report_xlsx()
                     
