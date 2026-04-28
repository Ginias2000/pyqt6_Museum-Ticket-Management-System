"""
Modern Widgets - Custom styled GUI components
"""

from PyQt6.QtWidgets import (
    QLineEdit, QPushButton, QComboBox, QWidget,
    QVBoxLayout, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QColor, QPalette


class ModernLineEdit(QLineEdit):
    """Modern styled line edit with placeholder animation"""
    
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(40)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 8px;
                padding: 8px 12px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #4a6cf7;
            }
            QLineEdit:hover {
                border-color: #5d7ef8;
            }
        """)
    
    def focusInEvent(self, event):
        """Animate on focus"""
        self.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e2f;
                border: 2px solid #4a6cf7;
                border-radius: 8px;
                padding: 8px 12px;
                color: #ffffff;
                font-size: 13px;
            }
        """)
        super().focusInEvent(event)
    
    def focusOutEvent(self, event):
        """Revert animation on focus out"""
        self.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 8px;
                padding: 8px 12px;
                color: #ffffff;
                font-size: 13px;
            }
        """)
        super().focusOutEvent(event)


class ModernButton(QPushButton):
    """Modern animated button with hover effects"""
    
    def __init__(self, text: str = "", icon: str = "", variant: str = "primary", parent=None):
        super().__init__(text, parent)
        self.variant = variant
        self.icon_text = icon
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Animation setup
        self.animation = QPropertyAnimation(self, b"opacity")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        self._opacity = 1.0
        self.apply_styles()
    
    def apply_styles(self):
        """Apply variant-specific styles"""
        styles = {
            "primary": """
                QPushButton {
                    background-color: #4a6cf7;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #5d7ef8;
                }
                QPushButton:pressed {
                    background-color: #3a5ce5;
                }
            """,
            "secondary": """
                QPushButton {
                    background-color: #2a2a3a;
                    color: #ffffff;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #353548;
                }
                QPushButton:pressed {
                    background-color: #1f1f2d;
                }
            """,
            "danger": """
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """,
            "success": """
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #2ecc71;
                }
            """
        }
        
        self.setStyleSheet(styles.get(self.variant, styles["primary"]))
        
        # Add icon if provided
        if self.icon_text:
            self.setText(f"{self.icon_text}  {self.text()}")
    
    def get_opacity(self):
        return self._opacity
    
    def set_opacity(self, opacity):
        self._opacity = opacity
        self.setGraphicsEffect(None)
        self.setStyleSheet(self.styleSheet() + f"opacity: {opacity};")
    
    opacity = pyqtProperty(float, get_opacity, set_opacity)
    
    def enterEvent(self, event):
        """Animate on hover enter"""
        self.animation.stop()
        self.animation.setEndValue(0.85)
        self.animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Animate on hover leave"""
        self.animation.stop()
        self.animation.setEndValue(1.0)
        self.animation.start()
        super().leaveEvent(event)


class ModernComboBox(QComboBox):
    """Modern styled combo box with dropdown animation"""
    
    def __init__(self, items: list = None, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(40)
        
        if items:
            self.addItems(items)
        
        self.setStyleSheet("""
            QComboBox {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 8px;
                padding: 8px 12px;
                color: #ffffff;
                font-size: 13px;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #5d7ef8;
            }
            QComboBox:focus {
                border-color: #4a6cf7;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #a0a0c0;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 8px;
                selection-background-color: #4a6cf7;
                color: #ffffff;
                padding: 4px;
            }
        """)


class ModernCard(QFrame):
    """Modern card widget with shadow effect"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("modern-card")
        self.setStyleSheet("""
            QFrame#modern-card {
                background-color: #252535;
                border-radius: 16px;
                border: 1px solid #2d2d3f;
            }
            QFrame#modern-card:hover {
                border-color: #4a6cf7;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                border: none;
            """)
            layout.addWidget(title_label)
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(10)
        layout.addLayout(self.content_layout)
    
    def add_widget(self, widget):
        """Add widget to card content"""
        self.content_layout.addWidget(widget)


class SearchBar(ModernLineEdit):
    """Search bar with search icon and clear functionality"""
    
    def __init__(self, parent=None):
        super().__init__("Search...", parent)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 20px;
                padding: 10px 16px;
                padding-left: 40px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #4a6cf7;
            }
        """)
        
        # Add search icon (simulated with text for now)
        self.setTextMargins(30, 0, 0, 0)
    
    def keyPressEvent(self, event):
        """Handle Enter key for search"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.parent().search(self.text()) if hasattr(self.parent(), 'search') else None
        super().keyPressEvent(event)