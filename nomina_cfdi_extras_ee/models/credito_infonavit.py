# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError

class CreditoInfonavit(models.Model):
    _name = 'credito.infonavit'
    _description = 'CreditoInfonavit'

    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    no_credito = fields.Char(string="Número de crédito")
    tipo_de_movimiento = fields.Selection([('15', 'Inicio de crédito vivienda'), 
                                          ('16', 'Fecha de suspensión de descuento'),
                                          ('17', 'Reinicio de descuento'),
                                          ('18', 'Modificación de tipo de descuento'),
                                          ('19', 'Modificación de valor de descuento'),
                                          ('20', 'Modificación de número de crédito'),],
                                            string='Tipo de movimiento')

    tipo_de_descuento = fields.Selection([('1', 'Porcentaje %'), 
                                          ('2', 'Cuota fija'),
                                          ('3', 'Veces SMGV'),],
                                            string='Tipo de movimiento', default='1')

    aplica_tabla = fields.Selection([('N', 'No'), 
                                     ('S', 'Si')],
                                     string='Aplica tabla disminución')
    fecha = fields.Date(string="Fecha")
    valor_descuento = fields.Float(string="Valor descuento", digits = (12,4))
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')], string='Estado', default='draft')
    contract_id = fields.Many2one('hr.contract', string='Contrato')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('credito.infonavit') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('credito.infonavit') or _('New')
        result = super(CreditoInfonavit, self).create(vals)
        return result

    def action_validar(self):
        self.write({'state':'done'})
        return

    def action_cancelar(self):
        self.write({'state':'cancel'})

    def action_draft(self):
        self.write({'state':'draft'})

    def action_change_state(self):
        for creditoinfonavit in self:
            if creditoinfonavit.state == 'draft':
                creditoinfonavit.action_validar()
