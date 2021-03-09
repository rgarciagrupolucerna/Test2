# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Grupo Lucerna Instance Creator',
    "version": "13.0.0.1",
    'summary': "AutoInstall Lucerna hired apps",
    'category': 'Instance Creator',
    'author': 'Grupo Lucerna',
    'license': 'LGPL-3',
    'depends': [
        # Odoo Apps
        'purchase',
        'purchase_requisition',
        # OCA
        # Free apps
        # Developments
    ],
    'data': [
        'views/purchase_views.xml',
    ],
}
