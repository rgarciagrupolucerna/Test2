# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from . import amount_to_text_es_MX
from datetime import datetime, timedelta, date

class Contract(models.Model):
    _inherit = "hr.contract"


    fecha_antiguedad = fields.Date('Fecha de inicio contrato')
    fecha_fin_contrato = fields.Date('Fecha fin de contrato')
    sueldo_promedio_lucerna = fields.Float('Sueldo promedio')

    sueldo_bruto = fields.Float(string="Sueldo bruto")
    sueldo_neto = fields.Float(string="Sueldo neto")

    compania_lucerna = fields.Char(string="Compañia")
    cedis_lucerna = fields.Char(string="CEDIS")
    ruta_lucerna = fields.Char(string="Ruta")
    diversos_lucerna = fields.Char(string="Diversos")
    cliente_lucerna = fields.Char(string="Cliente")
    producto_lucerna = fields.Char(string="Producto")
    depto_lucerna = fields.Selection([('GOP', 'GOP'), ('GIF', 'GIF'), ('CDP', 'CDP')], string='Depto. Lucerna')

    #ADD FIELD TIPO CONTRATO
    tipo_contrato_lucerna = fields.Selection(
        selection=[('01', 'Planta'), 
                   ('02', '60 Días'), 
                   ('03', '90 Días'),],
        string=_('Tipo de Contrato'),
        )

    categoria_lucerna = fields.Selection(
        selection=[('01', '1'),
                   ('02', '2'),
                   ('03', '3'),
                   ('04', '4'),
                   ('05', '5'),],
        string=_('Categoría'),
        )


    #Function to add days according to tipo_contrato_lucerna field


    @api.onchange('tipo_contrato_lucerna')
    def _check_tipo(self):
        if self.tipo_contrato_lucerna == '02':
            self.fecha_fin_contrato = self.fecha_antiguedad + timedelta(days=60)
        elif self.tipo_contrato_lucerna == '03':
            self.fecha_fin_contrato = self.fecha_antiguedad + timedelta(days=90)
        else:
            self.fecha_fin_contrato = False


    @api.onchange('wage')
    def _compute_sueldo(self):
        if self.wage:
            values = {
            'sueldo_diario': self.wage/30.4,
            'sueldo_hora': self.wage/30.4/8,
            'sueldo_diario_integrado': self.calculate_sueldo_diario_integrado(),
            'sueldo_base_cotizacion': self.calculate_sueldo_base_cotizacion(),
            }
            self.update(values)

    @api.model
    def calculate_sueldo_base_cotizacion(self): 
        if self.date_start: 
            today = datetime.today().date()
            diff_date = (today - self.date_start + timedelta(days=1)).days
            years = diff_date /365.0
            #_logger.info('years ... %s', years)
            tablas_cfdi = self.tablas_cfdi_id 
            if not tablas_cfdi: 
                tablas_cfdi = self.env['tablas.cfdi'].search([],limit=1) 
            if not tablas_cfdi:
                return 
            if years < 1.0: 
                tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad >= years).sorted(key=lambda x:x.antiguedad) 
            else: 
                tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad <= years).sorted(key=lambda x:x.antiguedad, reverse=True) 
            if not tablas_cfdi_lines: 
                return 
            tablas_cfdi_line = tablas_cfdi_lines[0]
            max_sdi = tablas_cfdi.uma * 25
            sdi = ((365 + tablas_cfdi_line.aguinaldo + (tablas_cfdi_line.vacaciones)* (tablas_cfdi_line.prima_vac/100) ) / 365 ) * self.wage/30.4
            if sdi > max_sdi:
                sueldo_base_cotizacion = max_sdi
            else:
                sueldo_base_cotizacion = sdi
        else: 
            sueldo_base_cotizacion = 0
        return sueldo_base_cotizacion

    @api.model
    def calculate_sueldo_diario_integrado(self): 
        if self.date_start: 
            today = datetime.today().date()
            diff_date = (today - self.date_start + timedelta(days=1)).days
            years = diff_date /365.0
            #_logger.info('years ... %s', years)
            tablas_cfdi = self.tablas_cfdi_id 
            if not tablas_cfdi: 
                tablas_cfdi = self.env['tablas.cfdi'].search([],limit=1) 
            if not tablas_cfdi:
                return 
            if years < 1.0: 
                tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad >= years).sorted(key=lambda x:x.antiguedad) 
            else: 
                tablas_cfdi_lines = tablas_cfdi.tabla_antiguedades.filtered(lambda x: x.antiguedad <= years).sorted(key=lambda x:x.antiguedad, reverse=True) 
            if not tablas_cfdi_lines: 
                return 
            tablas_cfdi_line = tablas_cfdi_lines[0]
            max_sdi = tablas_cfdi.uma * 25
            sdi = ((365 + tablas_cfdi_line.aguinaldo + (tablas_cfdi_line.vacaciones)* (tablas_cfdi_line.prima_vac/100.0) ) / 365.0 ) * self.wage/30.4
            sueldo_diario_integrado = sdi
        else: 
            sueldo_diario_integrado = 0
        return sueldo_diario_integrado

