# -*- coding: utf-8 -*-

from odoo import models
from collections import defaultdict
import io
import xlwt
import itertools
import base64

class PartnerXlsx(models.AbstractModel):
    _name = 'report.nomina_relacion_pagos.relacion_de_pagos_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, payslip_batches):
        for batche in payslip_batches:
            report_name = batche.name
            date_start = batche.date_start.strftime("%d/%m/%Y")
            date_end = batche.date_end.strftime("%d/%m/%Y")
            sheet = workbook.add_worksheet(report_name)
            bold = workbook.add_format({'bold': True})
            
#             workbook = xlwt.Workbook()
#             worksheet= workbook.add_sheet('Sheet 1')
#             col_width = 256 * 30
#             try:
#                 for i in itertools.count():
#                     worksheet.col(i).width = col_width
#             except ValueError:
#                 pass
            
            sheet.merge_range('B2:E2',    'Relación de pagos de nómina', bold)
            
            sheet.write(3, 4, 'Periodo', bold)
            sheet.write(3, 5, date_start + ' -', bold)
            sheet.write(3, 6, date_end, bold)

            sheet.write(6, 0, 'No. de empleado', bold)
            sheet.write(6, 1, 'Empleado', bold)
            sheet.write(6, 2, 'Percepciones', bold)
            sheet.write(6, 3, 'Deducciones', bold)
            sheet.write(6, 4, 'Total Efectivo', bold)
            sheet.write(6, 5, 'Total Especie', bold)
            sheet.write(6, 6, 'Pago total', bold)
            sheet.write(6, 7, 'Tipo de pago', bold)
           
            row_index = 7
            col_index = 0
            slip_lines = batche.slip_ids
            col1_tot = 0
            col2_tot = 0
            col3_tot = 0
            col4_efectivo = 0
            col5_especie = 0
            total_efectivo = 0
            total_especie = 0
            
            for slip_line in slip_lines:
                col1 = slip_line.get_amount_from_rule_code('TPER')
                col2 = slip_line.get_amount_from_rule_code('TDED')
                col3 = slip_line.get_amount_from_rule_code('NET')
                col4 = slip_line.get_amount_from_rule_code('TOP')
                col1_tot = col1_tot + col1 + col4
                col2_tot = col2_tot + col2
                col3_tot = col3_tot + col3
                col4_efectivo = slip_line.get_total_code_value('001')
                col5_especie = slip_line.get_total_code_value('002')
                total_efectivo = total_efectivo + col4_efectivo
                total_especie = total_especie + col5_especie
                
                tipo_pago_dict = dict(batche.slip_ids[0].employee_id._fields.get('tipo_pago').selection)
                tipo_pago = tipo_pago_dict.get(slip_line.employee_id.tipo_pago,'')

                sheet.write(row_index, col_index, slip_line.employee_id.no_empleado)
                col_index+=1
                sheet.write(row_index, col_index, slip_line.employee_id.name)
                col_index+=1
                sheet.write(row_index, col_index, '{:,}'.format(col1 + col4))
                col_index+=1
                sheet.write(row_index, col_index, '{:,}'.format(col2))
                col_index+=1
                sheet.write(row_index, col_index, '{:,}'.format(round(col4_efectivo,2)))
                col_index+=1
                sheet.write(row_index, col_index, '{:,}'.format(round(col5_especie,2)))
                col_index+=1
                sheet.write(row_index, col_index, '{:,}'.format(col3))
                col_index+=1
                sheet.write(row_index, col_index, tipo_pago)
                    
                row_index+=1
                col_index=0
            row_index+=1
            col_index+=1
            total_employee = len(batche.slip_ids.filtered(lambda x: x.state!='cancel').mapped('employee_id'))
            sheet.write(row_index, col_index, 'Total'+' '+str(total_employee)+' '+'Empleados', bold)
            col_index+=1
            sheet.write(row_index, col_index, '{:,}'.format(round(col1_tot,2)), bold)
            col_index+=1
            sheet.write(row_index, col_index, '{:,}'.format(round(col2_tot,2)), bold)
            col_index+=1
            sheet.write(row_index, col_index, '{:,}'.format(round(total_efectivo,2)), bold)
            col_index+=1
            sheet.write(row_index, col_index, '{:,}'.format(round(total_especie,2)), bold)
            col_index+=1
            sheet.write(row_index, col_index, '{:,}'.format(round(col3_tot,2)), bold)
            
            

                
                