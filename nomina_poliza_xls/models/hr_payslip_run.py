# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError
import io
from odoo.tools.misc import xlwt
import base64

from xlwt import easyxf
import logging
_logger = logging.getLogger(__name__)

class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    codigo_pasivo = fields.Char("Codigo pasivo")
    tipo_de_gasto = fields.One2many('nomina.cuenta.lucerna', 'doc_id', 'cta_gasto')
    nombre_alterno = fields.Char("Nombre alterno")

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    file_data = fields.Binary('File')

    def poliza_XLS(self):
        view = self.env.ref('nomina_poliza_xls.poliza_xls_wizard')
        ctx = self.env.context.copy()
        ctx .update({'default_payslip_batch_id':self.id})
        return {
            'name': 'Poliza XLS',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'poliza.xls',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': ctx,
        }
    def poliza_export_report_xlsx(self):
        #############################################################################################
        #############################################################################################
        # crear elementos de poliza
        #############################################################################################
        #############################################################################################
        for slip_batch in self:
            line_ids = []
            debit_sum = 0.0
            credit_sum = 0.0
            
            currency = slip_batch.journal_id.company_id.currency_id
            
           # payslips = payslip_obj.browse()
            start_range = self._context.get('start_range')
            end_range = self._context.get('end_range')
            for slip in slip_batch.slip_ids:
               # if start_range and end_range:
               #     if slip.employee_id.no_empleado:
               #         emp_no = int(slip.employee_id.no_empleado)
               #     if emp_no < start_range or emp_no > end_range:
               #         continue
                
               # if slip.move_id:
               #     continue
                for line in slip.details_by_salary_rule_category:
                    amount = currency.round(slip.credit_note and -line.total or line.total)
                   # if currency.is_zero(amount): #float_is_zero(amount, precision_digits=precision):
                   #     continue

                    #obtener la cuenta de pasivo
                    debit_account_id = False
                    debit_account_id = line.salary_rule_id.codigo_pasivo

                    #obtener la cuenta de gasto
                    credit_account_id = False
                    for department_id in line.salary_rule_id.tipo_de_gasto:
                        if not slip.employee_id.contract_id.depto_lucerna:
                            raise UserError(_('El empleado %s no tiene departamento configurado') % (slip.employee_id.name))
                        if slip.employee_id.contract_id.depto_lucerna == department_id.depto_lucerna:
                            credit_account_id = department_id.codigo_mayor

                    #if not debit_account_id and not credit_account_id:
                    #    raise UserError(_('La regla salarial %s no tiene cuentas de contabilidad configuradas') % ( line.name))

                    if debit_account_id:
                        if line.salary_rule_id.nombre_alterno:
                            nombre = line.salary_rule_id.nombre_alterno
                        else:
                            nombre = line.name
                        debit_line = {
                            'name': nombre,
                            'account_id': debit_account_id,
                            'debit': amount > 0.0 and amount or 0.0,
                            'credit': amount < 0.0 and -amount or 0.0,
                        }
                        line_ids.append(debit_line)
                        debit_sum += debit_line['debit'] - debit_line['credit']
                        _logger.info('debito %s', debit_line)
    
                    if credit_account_id:
                        contrato = slip.employee_id.contract_id
                        if not contrato.compania_lucerna or not contrato.cedis_lucerna or not contrato.ruta_lucerna or not contrato.diversos_lucerna or not contrato.cliente_lucerna or not contrato.producto_lucerna:
                            raise UserError(_('El contrato %s no tiene cuentas de contabilidad configuradas') % ( contrato.name))
                        if line.code == 'O001' or line.code == 'O007':
                            cuenta_lucerna = credit_account_id
                        else:
                            cuenta_lucerna = contrato.compania_lucerna + "-" + contrato.cedis_lucerna + "-" + contrato.ruta_lucerna + "-" + credit_account_id + "-" + \
                                         contrato.diversos_lucerna + "-" + contrato.cliente_lucerna + "-" + contrato.producto_lucerna
                        if line.salary_rule_id.nombre_alterno:
                            nombre = line.salary_rule_id.nombre_alterno
                        else:
                            nombre = line.name
                        credit_line = {
                            'name': nombre,
                            'account_id': cuenta_lucerna,
                            'debit': amount < 0.0 and -amount or 0.0,
                            'credit': amount > 0.0 and amount or 0.0,
                        }
                        line_ids.append(credit_line)
                        credit_sum += credit_line['credit'] - credit_line['debit']
                        _logger.info('credito %s', credit_line)
               # payslips += slip

            if currency.compare_amounts(credit_sum, debit_sum) == -1:
                #acc_id = slip_batch.journal_id.default_account_id.id
                #if not acc_id:
                #    raise UserError(_('Total credito %s --- Total debito %s') % ( credit_sum, debit_sum))
                adjust_credit = {
                    'name': _('Bancos'),
                    'account_id': "012-000-000-11298-000000-0000-00000",
                    'debit': 0.0,
                    'credit': currency.round(debit_sum - credit_sum),
                }
                line_ids.append(adjust_credit)
            elif currency.compare_amounts(debit_sum, credit_sum) == -1:
                #acc_id = slip_batch.journal_id.default_account_id.id
                #if not acc_id:
                #    raise UserError(_('Total credito %s --- Total debito %s') % ( credit_sum, debit_sum))
                adjust_debit = {
                    'name': _('Bancos'),
                    'account_id': "012-000-000-11298-000000-0000-00000",
                    'debit': currency.round(credit_sum - debit_sum),
                    'credit': 0.0,
                }
                line_ids.append(adjust_debit)

            line_group_by_account_name = {}
            for line in line_ids:
                account_id = line.get('account_id')
                line_name = line.get('name')
                group_key = (account_id,line_name)
                if group_key not in line_group_by_account_name:
                    line_group_by_account_name[group_key] = line
                else:
                    line_group_by_account_name[group_key].update({'credit' : line_group_by_account_name[group_key]['credit'] + line.get('credit')})
                    line_group_by_account_name[group_key].update({'debit' : line_group_by_account_name[group_key]['debit'] + line.get('debit')})
            line_ids = line_group_by_account_name.values()
                
        #############################################################################################
        #############################################################################################
        # crear archivo xls
        #############################################################################################
        #############################################################################################
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Listado de nomina')
        header_style = easyxf('font:height 200; align: horiz center; font:bold True;' "borders: top thin,left thin,right thin,bottom thin")
        header = easyxf('font:height 250; align: horiz center; font:bold True;' "borders: top thin,left thin,right thin,bottom thin")
        text_right = easyxf('font:height 200; align: horiz right;' "borders: top thin,bottom thin")
        bold = xlwt.easyxf("font: bold on; align: horiz center;")

        worksheet.write_merge(0, 0, 1, 4, self.env.user.company_id.name, header)
        worksheet.write_merge(1, 1, 1, 4, 'REPORTE POLIZA' , bold)
        worksheet.write(3, 0, 'Folio', header_style)
        worksheet.write(3, 1, 'Cuenta Contable', header_style)
        worksheet.write(3, 2, 'Monto del Cargo', header_style)
        worksheet.write(3, 3, 'Monto de Abono', header_style)
        worksheet.write(3, 4, 'Observaciones', header_style)
        row = 4
        col = 0
        
        number=0

        for item in line_ids:
            worksheet.write(row, col,number, text_right)
            col+=1
            worksheet.write(row, col,item.get('account_id'), text_right)
            col+=1
            worksheet.write(row, col,item.get('credit'), text_right)
            col+=1
            worksheet.write(row, col,item.get('debit'), text_right)
            col+=1
            worksheet.write(row, col,item.get('name'), text_right)
            row+=1
            col=0
            number+=1
        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        self.write({'file_data': base64.b64encode(data)})
        action = {
            'name': 'Poliza XLS',
            'type': 'ir.actions.act_url',
            'url': "/web/content/?model=hr.payslip.run&id=" + str(self.id) + "&field=file_data&download=true&filename=Poliza_XLS.xls",
            'target': 'self',
            }
        return action

class CuentasLucerna(models.Model):
    _name = "nomina.cuenta.lucerna"
    _description = 'Cuentas lucerna'

    doc_id = fields.Many2one('hr.salary.rule', 'Codigos Lucerna')
    depto_lucerna = fields.Selection([('GOP', 'GOP'), ('GIF', 'GIF'), ('CDP', 'CDP')], string='Depto. Lucerna')
    codigo_mayor = fields.Char("Codigo mayor gasto")

