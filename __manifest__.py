# -*- coding: utf-8 -*-
{
    'name': 'Comisiones PoS',
    'version': '1.0.0',
    'summary': 'Cálculo y seguimiento de comisiones por ventas en Punto de Venta',
    'category': 'Point of Sale',
    'author': 'Aurux',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'views/pos_commission_view.xml',
        'views/pos_commission_menu.xml',
        'data/server_action.xml',
        'report/pos_commission_report.xml',
        'report/pos_commission_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}