# -*- coding: utf-8 -*-
{
    "name": "sid_purchase_delay_sync",
    "version": "15.0.1.0.0",
    "category": "Purchases",
    "summary": "Calculo de retraso por linea de compra y sincronizacion a venta.",
    "author": "oscarsidsa81",
    "license": "LGPL-3",
    "post_init_hook": "post_init_fill_sid_has_po_delay",
    "depends": [
        "purchase",
        "oct_fecha_contrato_compras"
    ],
    "data": [
        "views/purchase_order_delay_column.xml",
        "views/form_order_line_tree_decoration.xml",
        "views/sale_order_form_and_tree_boolean.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sid_purchase_delay_sync/static/src/scss/purchase_delay.scss",
        ],
    },
    "installable": True,
    "application": False,
}
