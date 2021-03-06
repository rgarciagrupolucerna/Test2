# -*- coding: utf-8 -*-

from odoo import models

class EmplpyeeXlsx(models.AbstractModel):
    _name = 'report.nomina_lucerna.dispersion_de_bancos_xls'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, payslip_batches):
        for batche in payslip_batches:
            report_name = batche.name
            sheet = workbook.add_worksheet(report_name)
            bold = workbook.add_format({'bold': True})
            
            sheet.write(0, 0, 'No. de Empleado', bold)
            sheet.write(0, 1, 'Apellito Paterno Dispersion', bold)
            sheet.write(0, 2, 'Apellito Materno Dispersion', bold)
            sheet.write(0, 3, 'Nombre Dispersion', bold)
            sheet.write(0, 4, 'Numero de Cuenta', bold)
            sheet.write(0, 5, 'Total Dispersion', bold)
            sheet.write(0, 6, 'Tipo de Pago', bold)
            
            row = 1
            for payslip in batche.slip_ids:
                if payslip.employee_id and payslip.employee_id.tipo_pago == 'transferencia':
                    no_empleado = payslip.employee_id.no_empleado or ''
                    paterno = payslip.employee_id.dispersion_paterno or ''
                    materno = payslip.employee_id.dispersion_materno or ''
                    nombre = payslip.employee_id.dispersion_nombre or ''
                    no_cuenta = payslip.employee_id.no_cuenta or ''
                    tipo_de_pago = 'Transferencia' if payslip.employee_id.tipo_pago == 'transferencia' else ''
                    
                    total = 0.0
                    lines = payslip.line_ids.filtered(lambda r: r.code == 'EFECT') or []
                    for line in lines:
                        total += line.total
                    
                    sheet.write(row, 0, no_empleado)
                    sheet.write(row, 1, paterno)
                    sheet.write(row, 2, materno)
                    sheet.write(row, 3, nombre)
                    sheet.write(row, 4, no_cuenta)
                    sheet.write(row, 5, total)
                    sheet.write(row, 6, tipo_de_pago)
                    row += 1
                    
                    
                    