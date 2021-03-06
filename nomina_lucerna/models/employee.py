from odoo import api, fields, models, _
from . import amount_to_text_es_MX

class Employee(models.Model):
    _inherit = "hr.employee"
    
    no_tarjeta_despensa = fields.Char(_('No. Tarjeta Despensa'))
    clabe_interbancaria_lucerna = fields.Char('CLABE')

    tipo_contrato_lucerna = fields.Selection(
        selection=[('01', 'Planta'), 
                   ('02', '30 Días'), 
                   ('03', '90 Días'),],
        string=_('Tipo de Contrato'),
        )

    no_empleado = fields.Char(string='Número de empleado', required=True, copy=False, #readonly=True,
                           index=True, default=lambda self: _('New'))


    credencial_empleado = fields.Text()

    #_sql_constraints = [('unique_tarjeta', 'unique(no_tarjeta_despensa)', 'Número de despensa ya registrada'),
    #                     ('unique_cuenta', 'unique(no_cuenta)', 'Número de cuenta ya registrada')]


    @api.model
    def create(self, vals):
        if vals.get('no_empleado', _('New')) == _('New'):
            vals['no_empleado'] = self.env['ir.sequence'].next_by_code('hr.employee') or _('New')
        result = super(Employee, self).create(vals)
        return result


    amount_to_text = fields.Char('Amount to Text', compute='_get_amount_to_text',
                                 size=256, 
                                 help='Amount of the sueldo diario in letter')

    @api.depends('contract_id')
    def _get_amount_to_text(self):
        for record in self:
            record.amount_to_text = amount_to_text_es_MX.get_amount_to_text(record, contract_id.sueldo_diario,record.company_id.currency_id.name)
        
    @api.model
    def _get_amount_2_text(self, contract_id):
        return amount_to_text_es_MX.get_amount_to_text(self, contract_id, self.company_id.currency_id.name)
	
    @api.model
    def _get_dias_aguinaldo(self, contract_id):
        years = contract_id.antiguedad_anos

        if years < 1.0: 
            tablas_cfdi_lines = contract_id.tablas_cfdi_id.tabla_antiguedades.filtered(lambda x: x.antiguedad >= years).sorted(key=lambda x:x.antiguedad) 
        else: 
            tablas_cfdi_lines = contract_id.tablas_cfdi_id.tabla_antiguedades.filtered(lambda x: x.antiguedad <= years).sorted(key=lambda x:x.antiguedad, reverse=True) 
        if not tablas_cfdi_lines: 
            return 0
        return tablas_cfdi_lines[0].aguinaldo
