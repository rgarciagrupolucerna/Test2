# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, date
from collections import defaultdict
from dateutil.parser import parse

class ReporteDeAsistencia(models.TransientModel):
    _name = 'reporte.de.asistencia'
    _description = 'Reporte De Asistencia'
    
    start_date = fields.Date(string='Fecha Inicio')
    end_date = fields.Date(string='Fecha Fin')
    semana = fields.Char(string='Semana')
    department_ids = fields.Many2many('hr.department', string='Departamento', default=lambda self: self.env['hr.department'].search([]))
    
    
    def print_reporte_de_asistencia(self):
        self.ensure_one()
        [data] = self.read()
        active_ids = self.env.context.get('active_ids', [])
        data = {
            'ids': active_ids,
            'model': 'hr.employee',
            'form': data
        }
        employees = self.env['hr.employee'].search([('department_id','in',self.department_ids.ids)])
        department_dict = {}
        for emp in employees:
            if emp.department_id.id in department_dict:
                department_dict[emp.department_id.id].append(emp.id)
            else:
                department_dict.update({emp.department_id.id: [emp.id]})
        data['departments'] = department_dict
        return self.env.ref('nomina_lucerna.asistencia_report').report_action(self, data=data)
        
        

        