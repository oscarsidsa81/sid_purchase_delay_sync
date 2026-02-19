# sid_purchase_delay_sync

## Proposito
Modulo funcional que calcula `sid_po_line_delay` en `purchase.order.line` (compute/store) en base a:
- `contract_date` (prioritario)
- `estimated_date` (alternativo)
- Solo aplica si la linea esta pendiente (`pending_line == "true"`).

Ademas sincroniza en `sale.order.line` el boolean `sid_has_po_delay` cuando la linea de compra asociada entra en retraso.

## Hook
Incluye `post_init_hook` (`post_init_fill_sid_has_po_delay`) para rellenar:
- `pending_line`
- `sid_po_line_delay`
- `sid_has_po_delay`

en instalaciones/migraciones.

## Dependencias
- `sid_purchase_core` (define `pending_line` y campos base)
- `sid_sale_line_custom_fields` (flag en venta)
- `oct_fecha_contrato_compras`


## Visualizacion de retraso en compras
La columna `sid_po_line_delay` en lineas de compra aplica color al fondo de toda la fila y mantiene un `badge` con color fuerte para reforzar la severidad:
- `Retraso + de un mes`: rojo intenso.
- `Retraso 4 semanas` y `Retraso 1-2 semanas`: naranja.
- `Retraso 1 semana`: azul petroleo.
- `Quedan 2 dias`: gris pizarra.
- `Quedan 7/14/30 dias` y `+30 dias`: verde.

Los estilos viven en `static/src/scss/purchase_delay.scss` y se cargan en `web.assets_backend`.
