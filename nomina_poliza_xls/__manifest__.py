# -*- coding: utf-8 -*-
{
    'name': "Nomina Poliza xls",

    'summary': """
        """,

    'description': """
       
    """,

    'author': "IT Admin",

    'category': 'sale',
    'version': '14.07',
    'depends': ['hr','om_hr_payroll','nomina_cfdi_ee', 'om_hr_payroll_account','nomina_cfdi_conta_ee'],
    'data': [
       'views/hr_payroll_payslip_view.xml',
       'security/ir.model.access.csv',
       'wizard/poliza_xls_wizard_views.xml',
    ],
    
}
