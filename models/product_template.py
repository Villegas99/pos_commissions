# -*- coding: utf-8 -*-
from odoo import models, fields, api

# Reglas de negocio: {nombre_categoria: umbral_minimo_precio}
COMMISSION_RULES = {
    'Armazones': 800.0,
    'Micas/Lentes': 1500.0,
    'Lentes de contacto': 800.0,
}

COMMISSION_PERCENTAGE = 5.0


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_studio_genera_comision = fields.Boolean(
        string='Genera Comisión',
        compute='_compute_x_studio_commission',
        store=True,
        readonly=True,
        help='Calculado automáticamente según categoría y precio de lista.',
    )
    x_studio_porcentaje_comision = fields.Float(
        string='Porcentaje de Comisión (%)',
        compute='_compute_x_studio_commission',
        store=True,
        readonly=True,
        digits=(5, 2),
        help='Calculado automáticamente según categoría y precio de lista.',
    )

    @api.depends('list_price', 'categ_id', 'categ_id.name')
    def _compute_x_studio_commission(self):
        for product in self:
            categ_name = (product.categ_id.name or '').strip()
            threshold = COMMISSION_RULES.get(categ_name)
            if threshold is not None and product.list_price > threshold:
                product.x_studio_genera_comision = True
                product.x_studio_porcentaje_comision = COMMISSION_PERCENTAGE
            else:
                product.x_studio_genera_comision = False
                product.x_studio_porcentaje_comision = 0.0