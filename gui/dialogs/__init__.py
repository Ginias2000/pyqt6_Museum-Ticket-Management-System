"""
Dialogs Module - Modal dialog windows
"""

from .ticket_sale_dialog import TicketSaleDialog
from .visitor_entry_dialog import VisitorEntryDialog
from .config_dialog import ConfigDialog
from .statistics_dialog import StatisticsDialog

__all__ = [
    'TicketSaleDialog',
    'VisitorEntryDialog',
    'ConfigDialog',
    'StatisticsDialog'
]