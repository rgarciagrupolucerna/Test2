# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    def button_sent_to_approve(self):
        for po in self:
            if po.requisition_id.type_id.exclusive == 'exclusive':
                others_po = po.requisition_id.mapped('purchase_ids').filtered(lambda r: r.id != po.id)
                others_po.button_cancel()

            po.write({'state': 'to approve'})
        return {}
