from . import models

# Expose post-init hook at addon package level (Odoo expects it here).
from .hooks import post_init_fill_sid_has_po_delay
