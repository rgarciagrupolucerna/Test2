# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import date
from datetime import datetime


class OpenAcademyCourse(models.Model):
    _name = 'liquidaciones.liquida'
    _description = '''Liquidaciones'''

    #name = fields.Char(string="Title", required=True)
    description = fields.Text()

    responsible_id = fields.Many2one(
        'res.users',
        string="Responsible", 
        index=True,
        ondelete='set null',
        default=lambda self, *a: self.env.uid
    )
    ruta = fields.Many2one(
        'stock.location',
        string="Ruta",
        index=True,
        ondelete='set null',
        default=lambda self, *a: self.env.uid
    )
    #date_today = fields.Date(string='Date', compute='_get_date_today', store=True, readonly=True)
    date_today = fields.Date(default=fields.Date.today)
    productos_ids = fields.Many2many('stock.picking', domain="[('create_date', '>=', (context_today().strftime('%Y-%m-%d 00:00:00'))),('location_id', '=', 'WH/Stock'),('location_dest_id', '=', ruta)]", string="Inventario")
    #devolucion_ids = fields.Many2many('stock.quant', domain="[('location_id', '=', ruta)]", string="Inventario")
    devolucion_ids = fields.Many2many(comodel_name='stock.picking', relation='table_name', column1='col_name', column2='other_col_name', domain="[('create_date', '>=', (context_today().strftime('%Y-%m-%d 00:00:00'))),('location_id', '=', ruta),('location_dest_id', '=', 'Physical Locations/DEVOLUCION')]")
    merma_ids = fields.Many2many(comodel_name='stock.picking', relation='table_name2', column1='col_name2', column2='other_col_name2', domain="[('create_date', '>=', (context_today().strftime('%Y-%m-%d 00:00:00'))),('location_id', '=', ruta),('location_dest_id', '=', 'Physical Locations/MERMA')]")
    #FALTA FILTRAR POR RUTA
    remisiones_ids = fields.Many2many('sale.order', domain="[('create_date', '>=', (context_today().strftime('%Y-%m-%d 00:00:00'))),('ruta', '=', '72'),('payment_term_id', '=', 1)]", string="Contados")
    remisiones_creditos_ids = fields.Many2many(comodel_name='sale.order', relation='table_name3', column1='col_name3', column2='other_col_name3', domain="[('create_date', '>=', (context_today().strftime('%Y-%m-%d 00:00:00'))),('ruta', '=', '72'),('payment_term_id', '=', 3)]", string="Creditos")


    #remisiones_ids = fields.Many2many('sale.order', domain = "[('date_order', '=', datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')),('date_order', '=', datetime.datetime.now().strftime('%Y-%m-%d 23:23:59'))]", string="Remisiones")
    total = fields.Float(string='Total Inventario', readonly=False, compute='_compute_total')
    #total_contados = fields.Float(string='Contados', readonly=False, compute='_compute_total_contados')
    total_devolucion = fields.Float(string='Total Devolucion', readonly=False, compute='_compute_total_devolucion')
    total_merma = fields.Float(string='Total Merma', readonly=False, compute='_compute_total_merma')
    diferencia = fields.Float(string='Diferencia', readonly=False)

    #Notebook Resumen
    total_creditos = fields.Float(string='Creditos', readonly=False, compute='_compute_total_creditos')
    total_contados = fields.Float(string='Contados', readonly=False, compute='_compute_total_contados')
    total_notas_credito = fields.Float(string='Notas de Credito', readonly=False)
    total_efectivo= fields.Float(string='Efectivo', readonly=False)
    total_dolares = fields.Float(string='Dolares', readonly=False)
    total_cheques = fields.Float(string='Cheques', readonly=False)
    total_sobrantes_faltantes = fields.Float(string='Sobrantes y/o Faltantes', readonly=False)

    # Notebook Efectivo
    moneda05c = fields.Integer(string='Moneda de $.05', readonly=False)
    total_moneda05c = fields.Float(string='Total Moneda de $.05', readonly=True)

    moneda10c = fields.Integer(string='Moneda de $.10', readonly=False)
    total_moneda10c = fields.Float(string='Total Moneda de $.10', readonly=True)

    moneda20c = fields.Integer(string='Moneda de $.20', readonly=False)
    total_moneda20c = fields.Float(string='Total Moneda de $.20', readonly=True)

    moneda50c = fields.Integer(string='Moneda de $.50', readonly=False)
    total_moneda50c = fields.Float(string='Total Moneda de $.50', readonly=True)

    moneda1 = fields.Integer(string='Moneda de $1', readonly=False)
    total_moneda1 = fields.Float(string='Total Moneda de $1', readonly=True)

    moneda2 = fields.Integer(string='Moneda de $2', readonly=False)
    total_moneda2 = fields.Float(string='Total Moneda de $2', readonly=True)

    moneda5 = fields.Integer(string='Moneda de $5', readonly=False)
    total_moneda5 = fields.Float(string='Total Moneda de $5', readonly=True)

    moneda10 = fields.Integer(string='Moneda de $10', readonly=False)
    total_moneda10 = fields.Float(string='Total Moneda de $10', readonly=True)

    moneda20 = fields.Integer(string='Moneda de $20', readonly=False)
    total_moneda20 = fields.Float(string='Total Moneda de $20', readonly=True)

    moneda50 = fields.Integer(string='Moneda de $50', readonly=False)
    total_moneda50 = fields.Float(string='Total Moneda de $50', readonly=True)

    moneda100 = fields.Integer(string='Moneda de $100', readonly=False)
    total_moneda100 = fields.Float(string='Total Moneda de $100', readonly=True)

    moneda200 = fields.Integer(string='Moneda de $200', readonly=False)
    total_moneda200 = fields.Float(string='Total Moneda de $200', readonly=True)

    moneda500 = fields.Integer(string='Moneda de $500', readonly=False)
    total_moneda500 = fields.Float(string='Total Moneda de $500', readonly=True,compute='_compute_efectivo')

    moneda1000 = fields.Integer(string='Moneda de $1000', readonly=False)
    total_moneda1000 = fields.Float(string='Total Moneda de $1000', readonly=True)
    #Termina Notebook Efectivo



    @api.onchange('moneda05c','moneda10c','moneda05c','moneda20c','moneda1','moneda2','moneda5','moneda10','moneda20','moneda50','moneda100','moneda200','moneda500','moneda1000')
    def _compute_efectivo(self):
        self.total_moneda05c = self.moneda05c * .05
        self.total_moneda10c = self.moneda10c * .10
        self.total_moneda20c = self.moneda20c * .20
        self.total_moneda1 = self.moneda1 * 1
        self.total_moneda2 = self.moneda2 * 2
        self.total_moneda5 = self.moneda5 * 5
        self.total_moneda10 = self.moneda10 * 10
        self.total_moneda20 = self.moneda20 * 20
        self.total_moneda50 = self.moneda50 * 50
        self.total_moneda100 = self.moneda100 * 100
        self.total_moneda200 = self.moneda200 * 200
        self.total_moneda500 = self.moneda500 * 500
        self.total_moneda1000 = self.moneda1000 * 1000
        self.total_efectivo = self.total_moneda05c + self.total_moneda10c + self.total_moneda20c + self.total_moneda1 +self.total_moneda2+self.total_moneda5+self.total_moneda10+ self.total_moneda20+self.total_moneda50+ self.total_moneda100+self.total_moneda200+self.total_moneda500+self.total_moneda1000

    #@api.depends('productos_ids2')
    #def _compute_total2(self):
    #    for rec in self:
    #        total6 = sum(rec.productos_ids2.mapped('move_line_ids_without_package.x_studio_precio')) if rec.productos_ids2 else 0
    #        rec.totaltest = total6

    #PARA QUE ESTA FUNCION NO ENVIE ERROR FORZOZAMENTE HAY QUE CREAR EL CAMPO CON STUDIO Y COMPUTAR EL CAMPO STUDIOTOTAL
    @api.depends('productos_ids')
    def _compute_total(self):
        for rec in self:
            total2 = sum(rec.productos_ids.mapped('move_line_ids_without_package.x_studio_total_1')) if rec.productos_ids else 0
            rec.total = total2

    @api.depends('remisiones_ids')
    def _compute_total_contados(self):
        for rec in self:
            total3 = sum(rec.remisiones_ids.mapped('amount_total')) if rec.remisiones_ids else 0
            rec.total_contados = total3

    @api.depends('remisiones_creditos_ids')
    def _compute_total_creditos(self):
        for rec in self:
            total3 = sum(rec.remisiones_creditos_ids.mapped('amount_total')) if rec.remisiones_creditos_ids else 0
            rec.total_creditos = total3

    @api.depends('devolucion_ids')
    def _compute_total_devolucion(self):
        for rec in self:
            total4 = sum(rec.devolucion_ids.mapped('move_line_ids_without_package.x_studio_total_1')) if rec.devolucion_ids else 0
            rec.total_devolucion = total4

    @api.depends('merma_ids')
    def _compute_total_merma(self):
        for rec in self:
            total5 = sum(rec.merma_ids.mapped('move_line_ids_without_package.x_studio_total_1')) if rec.merma_ids else 0
            rec.total_merma = total5

    #En esta funcion, ir agregandotodo lo que se tenga que ir restando como precios especiales etc
    #@api.depends('total','total_contados','total_efectivo','total_devolucion','total_merma')
    #def _compute_diferencia(self):
    #    self.diferencia = self.total-self.total_contados-self.total_creditos-self.total_efectivo-self.total_devolucion-self.total_merma

    @api.onchange('total', 'total_contados', 'total_creditos', 'total_efectivo', 'total_devolucion', 'total_merma','total_notas_credito')
    def _compute_diferencia(self):
        self.diferencia = self.total - self.total_contados-self.total_creditos - self.total_efectivo - self.total_devolucion - self.total_merma







