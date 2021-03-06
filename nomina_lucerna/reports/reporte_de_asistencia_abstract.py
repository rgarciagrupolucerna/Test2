# -*- encoding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ReporteDeAsistenciaTemplate(models.AbstractModel):
    _name = 'report.nomina_lucerna.report_de_asistencia_template'
    _description = 'Asistencia Report'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        start_date = end_date = ''
        if docs.start_date:
            start_date = docs.start_date.strftime("%d-%m-%Y")
        if docs.end_date:
            end_date = docs.end_date.strftime("%d-%m-%Y")
        semana = docs.semana or ''
        company = self.env.company or ''
        
        return {
            'doc_ids': data['ids'],
            'doc_model': 'reporte.de.asistencia',
            'docs': docs,
            'data': data['departments'] if data.get('departments') else data,
            'start_date': start_date or '',
            'end_date': end_date or '',
            'semana': semana,
            'company': company,
        }
    
    
    
        