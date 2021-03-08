# -*- coding: utf-8 -*-
{
    "name": "Nomina CFDI Despensa",
    "author": "IT Admin",
    "version": "14.1",
    "category": "Other",
    "description":"Genera despensa para la nómina.",
    "depends": ["nomina_cfdi_ee",'om_hr_payroll','hr','report_xlsx', 'nomina_lucerna'],
    "data": [
    #    'security/ir.model.access.csv',
        'wizard/report_despensa.xml',
    ],
    "license": 'AGPL-3',
    'installable': True,
    'images': [''],
}
