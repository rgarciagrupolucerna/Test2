# -*- coding: utf-8 -*-
from odoo import models, fields, _, api

class PrimaDominical(models.Model):
    _name = 'prima.dominical'
    _description = 'PrimaDominical'

    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    fecha_primad = fields.Date('Fecha')
    
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')], string='Estado', default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('prima.dominical') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('prima.dominical') or _('New')
        result = super(PrimaDominical, self).create(vals)
        return result
    
   
    def action_validar(self):
        self.write({'state':'done'})
        return

   
    def action_cancelar(self):
        self.write({'state':'cancel'})
   
    def action_draft(self):
        self.write({'state':'draft'})

    def action_change_state(self):
        for primad in self:
            if primad.state == 'draft':
                #print('ESTADO')
                primad.action_validar()
