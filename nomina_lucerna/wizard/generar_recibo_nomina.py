# -*- encoding: utf-8 -*-

from odoo import models, fields

class GenerarReciboNomina(models.TransientModel):
    _name='generar.recibo.nomina'
    _description = 'Generar recibo de nomina'

    department_ids = fields.Many2many('hr.department',string="Departamento" ,  default=lambda self: self.env['hr.department'].search([]))
    employee_id = fields.Many2one("hr.employee",string="Empleado")

    #Function to print the report of recibo nomina by employee department
    def print_recibo_nomina(self):
        self.ensure_one()
        [data] = self.read() 
        ctx = self._context.copy()
        if ctx.get('active_ids') and ctx.get('active_model','')=='hr.payslip.run':
            payslips = self.env['hr.payslip.run'].browse(ctx.get('active_id')).slip_ids.filtered(lambda x: x.employee_id.department_id.id in self.department_ids.ids)
            if self.employee_id:
                payslips = payslips.filtered((lambda x:x.employee_id.id == self.employee_id.id)).filtered((lambda x:x.employee_id.department_id.id in self.department_ids.ids))
            #payslips = payslips.filtered(lambda x: x.employee_id).sorted(key=lambda x: x.employee_id.no_empleado)
            #payslips = payslips.sorted(key=lambda x: x.employee_id.no_empleado)
            payslips_line = payslips.line_ids.filtered(lambda x:x.code == 'NET' and x.amount > 0)
            payslips  = payslips_line.slip_id
            payslips = payslips.sorted(key=lambda x: x.employee_id.no_empleado)
#             datas = {
#                 'ids': [],
#                 'model': 'hr.payslip',
#                 'form': data
#             }
            return self.env.ref('nomina_lucerna.report_recibo_nomina').with_context(from_transient_model=True).report_action(payslips)
            
        