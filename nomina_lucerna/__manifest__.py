# -*- coding: utf-8 -*-
##############################################################################
#                 @author IT Admin
#
##############################################################################

{
    'name': 'Nomina Lucerna',
    'version': '1.8',
    'description': ''' Custom module for nomina lucerna
    ''',
    'category': 'Accounting',
    'author': 'IT Admin',
    'website': 'www.itadmin.com.mx',
    'depends': [
        'sale','account','nomina_cfdi_ee','om_hr_payroll','report_xlsx'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/generar_recibo_nomina.xml',
        'views/employee_view.xml',
        'views/contract_view.xml',
        'views/prima_dominical_view.xml',
        'views/descanso_laborado_view.xml',
        'data/sequence_data.xml',
        'reports/contrato_determinado.xml',
        'reports/contrato_indeterminado.xml',
        'reports/recibo_nomina.xml',
        'reports/carta_laboral.xml',
        'reports/imprimir_credencial.xml',
        #'reports/paperformat.xml',
        'views/hr_payslip_run.xml',
        'reports/dispersion_de_bancos.xml',
        'views/pension_alimenticia_view.xml',
        'wizard/reporte_de_asistencia_view.xml',
        'reports/reporte_de_asistencia_template.xml',
        'reports/reporte_de_asistencia.xml',
    ],

    'application': False,
    'installable': True,
    'price': 0.00,
    'currency': 'USD',
    'license': 'OPL-1',	
}
