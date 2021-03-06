# -*- coding: utf-8 -*-
from odoo import models, fields, _, api

class DescansoLaborado(models.Model):
    _name = 'descanso.laborado'
    _description = 'DescansoLaborado'

    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    fecha_descanso_laborado = fields.Date('Fecha')
    
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')], string='Estado', default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('descanso.laborado') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('descanso.laborado') or _('New')
        result = super(DescansoLaborado, self).create(vals)
        return result
    
   
    def action_validar(self):
        self.write({'state':'done'})
        return

   
    def action_cancelar(self):
        self.write({'state':'cancel'})
   
    def action_draft(self):
        self.write({'state':'draft'})

    def action_change_state(self):
        for descansol in self:
            if descansol.state == 'draft':
                #print('ESTADO')
                descansol.action_validar()
