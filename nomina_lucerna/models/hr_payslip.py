# -*- coding: utf-8 -*-

from odoo import api, models, fields, _

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    semana = fields.Selection(
        selection=[('01', '01'), 
                   ('02', '02'), 
                   ('03', '03'),
                   ('04', '04'), 
                   ('05', '05'),
                   ('06', '06'), 
                   ('07', '07'),
                   ('08', '08'), 
                   ('09', '09'), 
                   ('11', '11'),
                   ('12', '12'),
                   ('13', '13'),
                   ('14', '14'),
                   ('15', '15'),
                   ('16', '16'),
                   ('17', '17'),
                   ('18', '18'),
                   ('19', '19'),
                   ('20', '20'),
                   ('21', '21'),
                   ('22', '22'),
                   ('23', '23'),
                   ('24', '24'),
                   ('25', '25'),
                   ('26', '26'),
                   ('27', '27'),
                   ('28', '28'),
                   ('29', '29'),
                   ('30', '30'),
                   ('31', '31'),
                   ('32', '32'),
                   ('33', '33'),
                   ('34', '34'),
                   ('35', '35'),
                   ('36', '36'),
                   ('37', '37'),
                   ('38', '38'),
                   ('39', '39'),
                   ('40', '40'),
                   ('41', '41'),
                   ('42', '42'),
                   ('43', '43'),
                   ('44', '44'),
                   ('45', '45'),
                   ('46', '46'),
                   ('47', '47'),
                   ('48', '48'),
                   ('49', '49'),
                   ('50', '50'),
                   ('51', '51'),
                   ('52', '52'),],
        string=_('Semana'))

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    
    semana = fields.Selection(
        selection=[('01', '01'), 
                   ('02', '02'), 
                   ('03', '03'),
                   ('04', '04'), 
                   ('05', '05'),
                   ('06', '06'), 
                   ('07', '07'),
                   ('08', '08'), 
                   ('09', '09'), 
                   ('11', '11'),
                   ('12', '12'),
                   ('13', '13'),
                   ('14', '14'),
                   ('15', '15'),
                   ('16', '16'),
                   ('17', '17'),
                   ('18', '18'),
                   ('19', '19'),
                   ('20', '20'),
                   ('21', '21'),
                   ('22', '22'),
                   ('23', '23'),
                   ('24', '24'),
                   ('25', '25'),
                   ('26', '26'),
                   ('27', '27'),
                   ('28', '28'),
                   ('29', '29'),
                   ('30', '30'),
                   ('31', '31'),
                   ('32', '32'),
                   ('33', '33'),
                   ('34', '34'),
                   ('35', '35'),
                   ('36', '36'),
                   ('37', '37'),
                   ('38', '38'),
                   ('39', '39'),
                   ('40', '40'),
                   ('41', '41'),
                   ('42', '42'),
                   ('43', '43'),
                   ('44', '44'),
                   ('45', '45'),
                   ('46', '46'),
                   ('47', '47'),
                   ('48', '48'),
                   ('49', '49'),
                   ('50', '50'),
                   ('51', '51'),
                   ('52', '52'),],
        string=_('Semana'))

    def enviar_nomina_timbrada(self):
        self.ensure_one()
        ctx = self._context.copy()
        template = self.env.ref('nomina_cfdi_ee.email_template_payroll', False)
        for payslip in self.slip_ids:
            if payslip.estado_factura == 'factura_correcta':
                ctx.update({
                    'default_model': 'hr.payslip',
                    'default_res_id': payslip.id,
                    'default_use_template': bool(template),
                    'default_template_id': template.id,
                    'default_composition_mode': 'comment',
                })
            
                vals = self.env['mail.compose.message'].onchange_template_id(template.id, 'comment', 'hr.payslip', payslip.id)
                mail_message  = self.env['mail.compose.message'].with_context(ctx).create(vals.get('value',{}))
                mail_message.send_mail()
        return True