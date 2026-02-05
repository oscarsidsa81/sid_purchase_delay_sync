# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    sid_po_line_delay = fields.Selection(
        selection=[
            ("1_week_del", "Retraso 1 semana"),
            ("2_week_del", "Retraso 1-2 semanas"),
            ("4_week_del", "Retraso 4 semanas"),
            ("more_del", "Retraso + de un mes"),
            ("2_days", "Quedan 2 dias"),
            ("7_days", "Quedan 7 dias"),
            ("14_days", "Quedan 14 dias"),
            ("30_days", "Quedan 30 dias"),
            ("sin_ret", "+30 dias"),
        ],
        string="Retraso por item",
        compute="_compute_sid_po_line_delay",
        store=True,
        readonly=True,
    )

    @api.depends("contract_date", "estimated_date", "pending_line")
    def _compute_sid_po_line_delay(self):
        today = fields.Date.context_today(self)

        for line in self:
            if line.pending_line != "true":
                line.sid_po_line_delay = False
                continue

            base_date = line.contract_date or line.estimated_date
            if not base_date:
                line.sid_po_line_delay = False
                continue

            planned_date = fields.Date.to_date(base_date)
            diff_days = (planned_date - today).days

            if diff_days <= -31:
                line.sid_po_line_delay = "more_del"
            elif diff_days <= -28:
                line.sid_po_line_delay = "4_week_del"
            elif diff_days <= -14:
                line.sid_po_line_delay = "2_week_del"
            elif diff_days <= -7:
                line.sid_po_line_delay = "1_week_del"
            elif diff_days <= 2:
                line.sid_po_line_delay = "2_days"
            elif diff_days <= 7:
                line.sid_po_line_delay = "7_days"
            elif diff_days <= 14:
                line.sid_po_line_delay = "14_days"
            elif diff_days <= 30:
                line.sid_po_line_delay = "30_days"
            else:
                line.sid_po_line_delay = "sin_ret"

    def write(self, vals):
        track_keys = {
            "sid_po_line_delay",
            "contract_date",
            "estimated_date",
            "product_qty",
            "qty_received",
        }
        track = any(k in vals for k in track_keys)

        before = {}
        if track:
            for pol in self:
                before[pol.id] = pol.sid_po_line_delay

        res = super().write(vals)

        if track:
            self._sync_sale_delay_flag(before_map=before)

        return res

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines._sync_sale_delay_flag(before_map={})
        return lines

    def _sync_sale_delay_flag(self, before_map):
        SaleLine = self.env["sale.order.line"].sudo()
        updates = {}

        for pol in self:
            old = before_map.get(pol.id, None)
            new = pol.sid_po_line_delay

            if old is not None and old == new:
                continue

            sale_line = getattr(pol, "sale_line_id", False)
            if not sale_line:
                continue

            delay_is_late = new in ("1_week_del", "2_week_del", "4_week_del", "more_del")
            updates[sale_line.id] = delay_is_late

        if not updates:
            return

        for sale_line_id, flag in updates.items():
            SaleLine.browse(sale_line_id).write({"sid_has_po_delay": flag})
