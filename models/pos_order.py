# -*- coding: utf-8 -*-
from odoo import models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _create_x_studio_commission_records(self):
        """
        Crea registros de comisión para cada línea cuyo producto tenga
        x_studio_genera_comision = True en su plantilla.
        La comisión se asigna directamente al usuario de la orden (order.user_id).
        """
        commission_obj = self.env['pos.commission']

        for order in self:
            # Si la orden no tiene usuario asignado, no se puede generar comisión
            if not order.user_id:
                continue

            for line in order.lines:
                product = line.product_id
                tmpl = product.product_tmpl_id

                if not tmpl.x_studio_genera_comision:
                    continue

                percentage = tmpl.x_studio_porcentaje_comision
                if percentage <= 0:
                    continue

                # Evitar duplicados: si ya existe una comisión para esta línea, no crear otra
                existing = commission_obj.search([
                    ('x_studio_order_id', '=', order.id),
                    ('x_studio_product_id', '=', product.id),
                    ('x_studio_user_id', '=', order.user_id.id),
                ], limit=1)
                if existing:
                    continue

                commission_obj.create({
                    'x_studio_order_id': order.id,
                    'x_studio_product_id': product.id,
                    'x_studio_user_id': order.user_id.id,
                    'x_studio_date': order.date_order,
                    'x_studio_unit_price': line.price_unit,
                    'x_studio_quantity': line.qty,
                    'x_studio_percentage': percentage,
                    'x_studio_is_paid': False,
                    'x_studio_state': 'draft',
                })

    def create(self, vals_list):
        orders = super().create(vals_list)
        orders._create_x_studio_commission_records()
        return orders

    def action_pos_order_paid(self):
        result = super().action_pos_order_paid()
        self._create_x_studio_commission_records()
        return result