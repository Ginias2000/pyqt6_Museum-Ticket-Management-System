"""
Card Widget - Professional card-style container
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QFont


class CardWidget(QFrame):
    """Professional card widget with hover effects and animations"""
    
    clicked = pyqtSignal()
    
    def __init__(self, title: str = "", subtitle: str = "", icon: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("card-widget")
        self.setMinimumHeight(120)
        self.setMaximumWidth(300)
        
        self.setStyleSheet("""
            QFrame#card-widget {
                background-color: #252535;
                border-radius: 16px;
                border: 1px solid #2d2d3f;
            }
            QFrame#card-widget:hover {
                border-color: #4a6cf7;
                background-color: #2a2a3f;
            }
        """)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)
        
        # Icon section
        if icon:
            self.icon_label = QLabel(icon)
            self.icon_label.setStyleSheet("""
                font-size: 42px;
                background-color: #4a6cf720;
                border-radius: 12px;
                padding: 12px;
            """)
            self.icon_label.setFixedSize(70, 70)
            self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.icon_label)
        
        # Text section
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        
        if title:
            self.title_label = QLabel(title)
            title_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
            self.title_label.setFont(title_font)
            self.title_label.setStyleSheet("color: #ffffff; border: none;")
            text_layout.addWidget(self.title_label)
        
        if subtitle:
            self.subtitle_label = QLabel(subtitle)
            self.subtitle_label.setStyleSheet("color: #a0a0c0; font-size: 12px; border: none;")
            text_layout.addWidget(self.subtitle_label)
        
        text_layout.addStretch()
        layout.addLayout(text_layout, stretch=1)
        
        # Optional value label
        self.value_label = QLabel()
        value_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        self.value_label.setFont(value_font)
        self.value_label.setStyleSheet("color: #4a6cf7; border: none;")
        layout.addWidget(self.value_label)
        
        # Animation setup
        self.animation = QPropertyAnimation(self, b"hover_effect")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        self._hover_effect = 0
    
    @property
    def hover_effect(self):
        return self._hover_effect
    
    @hover_effect.setter
    def hover_effect(self, value):
        self._hover_effect = value
        self.setGraphicsEffect(None)
    
    def enterEvent(self, event):
        """Mouse enter animation"""
        self.animation.stop()
        self.animation.setEndValue(1)
        self.animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Mouse leave animation"""
        self.animation.stop()
        self.animation.setEndValue(0)
        self.animation.start()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Handle click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
    
    def set_value(self, value: str):
        """Set the value display"""
        self.value_label.setText(value)
    
    def set_title(self, title: str):
        """Set the card title"""
        self.title_label.setText(title)
    
    def set_subtitle(self, subtitle: str):
        """Set the card subtitle"""
        self.subtitle_label.setText(subtitle)


class StatsCard(CardWidget):
    """Statistics card with specific styling for metrics"""
    
    def __init__(self, title: str, value: str, icon: str, trend: str = "", color: str = "#4a6cf7", parent=None):
        super().__init__(title, icon=icon, parent=parent)
        self.set_value(value)
        self.setStyleSheet(f"""
            QFrame#card-widget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}20, stop:1 #252535);
                border-radius: 20px;
            }}
        """)
        
        if trend:
            trend_label = QLabel(trend)
            trend_color = "#27ae60" if "↑" in trend else "#e74c3c" if "↓" in trend else "#a0a0c0"
            trend_label.setStyleSheet(f"color: {trend_color}; font-size: 11px;")
            self.content_layout.addWidget(trend_label)


class TicketCard(CardWidget):
    """Card specifically for ticket display"""
    
    def __init__(self, ticket_id: str, ticket_type: str, price: float, status: str, parent=None):
        super().__init__(title=ticket_type, subtitle=f"ID: {ticket_id}", parent=parent)
        self.set_value(f"¥{price:.2f}")
        
        # Status badge
        status_colors = {
            "purchased": "#f39c12",
            "visiting": "#4a6cf7",
            "used": "#27ae60",
            "expired": "#e74c3c",
            "cancelled": "#95a5a6"
        }
        
        status_label = QLabel(status.upper())
        status_label.setStyleSheet(f"""
            background-color: {status_colors.get(status, '#95a5a6')};
            color: white;
            border-radius: 12px;
            padding: 4px 12px;
            font-size: 10px;
            font-weight: bold;
        """)
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_label.setMaximumWidth(80)
        self.content_layout.insertWidget(0, status_label)


class VisitorCard(CardWidget):
    """Card for displaying visitor information"""
    
    def __init__(self, name: str, id_number: str, entry_time: str = "", parent=None):
        super().__init__(title=name, subtitle=id_number, parent=parent)
        
        if entry_time:
            time_label = QLabel(f"Entry: {entry_time}")
            time_label.setStyleSheet("color: #a0a0c0; font-size: 11px;")
            self.content_layout.addWidget(time_label)