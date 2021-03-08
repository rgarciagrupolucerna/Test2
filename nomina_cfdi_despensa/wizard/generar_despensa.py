# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime, date
import base64
import xlwt
import logging
_logger = logging.getLogger(__name__)

class NominaDespensaCardXlsx(models.AbstractModel):
    _name = 'report.nomina_cfdi_despensa.report_nomina_despensa'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        row=0

        #REPORT HEADER 
        #for lines in data:
        sheet = workbook.add_worksheet('Nómina Despensa')
        sheet.write(row, 0, '3', )
        sheet.write(row, 1, '11', )
        sheet.write(row, 2, '32',)
        sheet.write(row, 3, '75796',)
        sheet.write(row, 4, '1',)
        sheet.write(row, 5, 'UNION DE GANADEROS LECHEROS',)
        #sheet.write(row, 6, 'TOTAL DE EMPLEADOS:',)
        #sheet.write(row, 7, 'TOTAL ESPECIE',)

            #REPORT BODY
        line_sum = 0.0
        for l in lines.slip_ids:
            row +=1
            sheet.write(row, 0, l.employee_id.no_empleado)
            sheet.write(row, 1, l.employee_id.no_tarjeta_despensa,)
            #sheet.write(row, 2, l.employee_id.contract_ids.vale_despensa_amount)
            for regla in l.line_ids:
                if regla.salary_rule_id.forma_pago == '002':
                    sheet.write(row, 2, regla.total)
                    line_sum += regla.total
                #else:
                #    sheet.write(row, 2, '0')

            #line_sum += l.employee_id.contract_ids.vale_despensa_amount

        #PRINT TOTAL ESPECIE
        sheet.write(0,7,line_sum)
        len_employees = len(lines.slip_ids)
        sheet.write(0,6,len_employees) 
