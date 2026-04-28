"""
Dashboard Page - Real-time statistics and overview
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from gui.widgets.card_widget import CardWidget


class StatCard(QFrame):
    """Modern statistics card with icon and value"""
    
    def __init__(self, title: str, value: str, icon: str, color: str = "#4a6cf7"):
        super().__init__()
        self.setObjectName("stat-card")
        self.setFixedHeight(140)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Left: Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 48px;
            background-color: {color}20;
            border-radius: 16px;
            padding: 12px;
        """)
        icon_label.setFixedSize(80, 80)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Right: Text
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        
        value_label = QLabel(value)
        value_label.setObjectName("stat-value")
        value_font = QFont("Segoe UI", 28, QFont.Weight.Bold)
        value_label.setFont(value_font)
        text_layout.addWidget(value_label)
        
        title_label = QLabel(title)
        title_label.setObjectName("stat-label")
        title_font = QFont("Segoe UI", 12)
        title_label.setFont(title_font)
        text_layout.addWidget(title_label)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        self.value_label = value_label
        
    def update_value(self, value: str):
        """Update the displayed value"""
        self.value_label.setText(str(value))


class DashboardPage(QWidget):
    """Dashboard page with statistics and overview"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        self.setup_refresh_timer()
        
    def setup_ui(self):
        """Setup dashboard UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(25)
        
        # Welcome section
        welcome_label = QLabel("Welcome to Museum Management System")
        welcome_label.setStyleSheet("font-size: 18px; color: #ffffff; font-weight: bold;")
        layout.addWidget(welcome_label)
        
        # Statistics cards grid
        self.cards_layout = QGridLayout()
        self.cards_layout.setSpacing(20)
        
        # Create stat cards
        self.stat_cards = {
            "total_visitors": StatCard("Total Visitors", "0", "👥", "#4a6cf7"),
            "today_visitors": StatCard("Today's Visitors", "0", "📅", "#27ae60"),
            "active_visitors": StatCard("Currently Inside", "0", "🏛️", "#e67e22"),
            "total_revenue": StatCard("Total Revenue", "¥0", "💰", "#f39c12"),
            "today_revenue": StatCard("Today's Revenue", "¥0", "💵", "#3498db"),
            "tickets_sold": StatCard("Tickets Sold", "0", "🎫", "#9b59b6"),
        }
        
        # Add cards to grid
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
        for i, (key, card) in enumerate(self.stat_cards.items()):
            row, col = positions[i]
            self.cards_layout.addWidget(card, row, col)
        
        layout.addLayout(self.cards_layout)
        
        # Quick actions section
        quick_actions_label = QLabel("Quick Actions")
        quick_actions_label.setStyleSheet("font-size: 16px; color: #ffffff; font-weight: bold; margin-top: 10px;")
        layout.addWidget(quick_actions_label)
        
        # Add some spacing
        layout.addStretch()
        
    def setup_refresh_timer(self):
        """Setup auto-refresh timer"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds
        self.refresh()
    
    def refresh(self):
        """Refresh all statistics"""
        try:
            stats = self.db_manager.get_total_statistics()
            
            self.stat_cards["total_visitors"].update_value(str(stats.get("total_visitors", 0)))
            self.stat_cards["today_visitors"].update_value(str(stats.get("today_visitors", 0)))
            self.stat_cards["active_visitors"].update_value(str(stats.get("active_visitors", 0)))
            self.stat_cards["total_revenue"].update_value(f"¥{stats.get('total_revenue', 0):,.2f}")
            self.stat_cards["today_revenue"].update_value(f"¥{stats.get('today_revenue', 0):,.2f}")
            self.stat_cards["tickets_sold"].update_value(str(stats.get("total_tickets_sold", 0)))
            
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")