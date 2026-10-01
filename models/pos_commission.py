# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PosCommission(models.Model):
    _name = 'pos.commission'
    _description = 'Registro de Comisión PoS'
    _order = 'x_studio_date desc, id desc'

    x_studio_order_id = fields.Many2one(
        comodel_name='pos.order',
        string='Orden PoS',
        required=True,
        ondelete='cascade',
        readonly=True,
    )
    x_studio_product_id = fields.Many2one(
        comodel_name='product.product',
        string='Producto',
        required=True,
        ondelete='restrict',
        readonly=True,
    )
    x_studio_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Usuario',
        required=True,
        ondelete='restrict',
        readonly=True,
    )
    x_studio_date = fields.Datetime(
        string='Fecha',
        required=True,
        readonly=True,
    )
    x_studio_unit_price = fields.Float(
        string='Precio Unitario',
        digits=(16, 2),
        readonly=True,
    )
    x_studio_quantity = fields.Float(
        string='Cantidad',
        digits=(16, 2),
        readonly=True,
    )
    x_studio_percentage = fields.Float(
        string='Porcentaje (%)',
        digits=(5, 2),
        readonly=True,
    )
    x_studio_commission_amount = fields.Float(
        string='Monto de Comisión',
        compute='_compute_x_studio_commission_amount',
        store=True,
        digits=(16, 2),
        readonly=True,
    )
    x_studio_is_paid = fields.Boolean(
        string='Pagado',
        default=False,
        readonly=True,
    )
    x_studio_state = fields.Selection(
        selection=[
            ('draft', 'Borrador'),
            ('paid', 'Pagado'),
        ],
        string='Estado',
        default='draft',
        required=True,
        readonly=True,
    )

    @api.depends('x_studio_unit_price', 'x_studio_quantity', 'x_studio_percentage')
    def _compute_x_studio_commission_amount(self):
        for record in self:
            record.x_studio_commission_amount = (
                record.x_studio_unit_price
                * record.x_studio_quantity
                * (record.x_studio_percentage / 100.0)
            )

    def action_x_studio_mark_as_paid(self):
        """
        Marca los registros seleccionados como pagados.
        Se usa sudo() para saltar el readonly de los campos a nivel de vista.
        """
        self.sudo().write({
            'x_studio_is_paid': True,
            'x_studio_state': 'paid',
        })