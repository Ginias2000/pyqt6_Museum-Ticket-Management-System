"""
Animated Button - Professional button with animations and effects
"""

from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QPoint, QTimer
from PyQt6.QtGui import QFont, QColor, QPainter, QBrush, QPen


class AnimatedButton(QPushButton):
    """Professional animated button with ripple effect and hover animations"""
    
    def __init__(self, text: str = "", icon: str = "", icon_position: str = "left", parent=None):
        super().__init__(text, parent)
        self.icon_text = icon
        self.icon_position = icon_position
        self.ripple_radius = 0
        self.ripple_alpha = 150
        self._pressed_pos = QPoint(-1, -1)
        
        self.setMinimumHeight(44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Setup animation
        self.scale_animation = QPropertyAnimation(self, b"scale_factor")
        self.scale_animation.setDuration(100)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        self._scale_factor = 1.0
        
        self.apply_style()
        self.update_text()
    
    def apply_style(self):
        """Apply base style"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #4a6cf7;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #5d7ef8;
            }
            QPushButton:pressed {
                background-color: #3a5ce5;
            }
            QPushButton:disabled {
                background-color: #3a3a4a;
                color: #6a6a80;
            }
        """)
    
    def update_text(self):
        """Update button text with icon"""
        if self.icon_text:
            if self.icon_position == "left":
                self.setText(f"{self.icon_text}  {self.text()}")
            else:
                self.setText(f"{self.text()}  {self.icon_text}")
    
    def get_scale_factor(self):
        return self._scale_factor
    
    def set_scale_factor(self, factor):
        self._scale_factor = factor
        # Apply transform scale
        self.setGraphicsEffect(None)
    
    scale_factor = pyqtProperty(float, get_scale_factor, set_scale_factor)
    
    def animate_press(self):
        """Animate button press"""
        self.scale_animation.stop()
        self.scale_animation.setEndValue(0.95)
        self.scale_animation.start()
        
        QTimer.singleShot(100, self.animate_release)
    
    def animate_release(self):
        """Animate button release"""
        self.scale_animation.stop()
        self.scale_animation.setEndValue(1.0)
        self.scale_animation.start()
    
    def mousePressEvent(self, event):
        """Handle mouse press with ripple effect"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed_pos = event.position().toPoint()
            self.ripple_radius = 0
            self.ripple_alpha = 150
            self.animate_press()
            self.update()  # Trigger paint for ripple
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        self._pressed_pos = QPoint(-1, -1)
        self.update()
        super().mouseReleaseEvent(event)
    
    def paintEvent(self, event):
        """Custom paint for ripple effect"""
        super().paintEvent(event)
        
        if self._pressed_pos.x() >= 0 and self.ripple_radius < 100:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Increase ripple radius
            self.ripple_radius += 15
            
            # Draw ripple
            painter.setBrush(QBrush(QColor(255, 255, 255, self.ripple_alpha)))
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            painter.drawEllipse(self._pressed_pos, self.ripple_radius, self.ripple_radius)
            
            # Schedule repaint for animation
            if self.ripple_radius < 100:
                QTimer.singleShot(16, self.update)
            else:
                self._pressed_pos = QPoint(-1, -1)


class IconButton(AnimatedButton):
    """Button with large icon and text below"""
    
    def __init__(self, icon: str, text: str, parent=None):
        super().__init__(text, icon, "top", parent)
        self.setMinimumHeight(80)
        self.setMinimumWidth(100)
        self.setStyleSheet("""
            QPushButton {
                background-color: #252535;
                border: 1px solid #2d2d3f;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #2a2a3f;
                border-color: #4a6cf7;
            }
        """)
    
    def update_text(self):
        """Custom layout for icon on top"""
        # For icon on top, we need to use a custom layout
        # Simplified version:
        self.setText(f"{self.icon_text}\n{self.text()}")
        self.setStyleSheet(self.styleSheet() + "padding: 12px;")


class LoadingButton(AnimatedButton):
    """Button with loading animation state"""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent=parent)
        self._is_loading = False
        self._original_text = text
        self._loading_index = 0
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self.update_loading_animation)
    
    def start_loading(self):
        """Start loading animation"""
        self._is_loading = True
        self.setEnabled(False)
        self.loading_timer.start(300)
    
    def stop_loading(self):
        """Stop loading animation"""
        self._is_loading = False
        self.loading_timer.stop()
        self.setText(self._original_text)
        self.setEnabled(True)
    
    def update_loading_animation(self):
        """Update loading dots animation"""
        if self._is_loading:
            dots = ["", ".", "..", "..."][self._loading_index]
            self.setText(f"{self._original_text}{dots}")
            self._loading_index = (self._loading_index + 1) % 4
    
    def mousePressEvent(self, event):
        """Prevent clicks while loading"""
        if not self._is_loading:
            super().mousePressEvent(event)


class ToggleButton(AnimatedButton):
    """Toggle button with ON/OFF states"""
    
    toggled = None  # Will be set as pyqtSignal
    
    def __init__(self, text_on: str = "ON", text_off: str = "OFF", parent=None):
        super().__init__(text_off, parent=parent)
        self.text_on = text_on
        self.text_off = text_off
        self._is_on = False
        
        self.apply_toggle_style()
    
    def apply_toggle_style(self):
        """Apply toggle-specific style"""
        self.setMinimumWidth(80)
        self.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                border-radius: 20px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
    
    def toggle(self):
        """Toggle button state"""
        self._is_on = not self._is_on
        
        if self._is_on:
            self.setText(self.text_on)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    border-radius: 20px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #2ecc71;
                }
            """)
        else:
            self.setText(self.text_off)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    border-radius: 20px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
        
        if self.toggled:
            self.toggled.emit(self._is_on)
    
    def mousePressEvent(self, event):
        """Toggle on click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle()
        super().mousePressEvent(event)
    
    def set_checked(self, checked: bool):
        """Set checked state programmatically"""
        if checked != self._is_on:
            self.toggle()


# Fix missing imports
from PyQt6.QtCore import pyqtSignal
ToggleButton.toggled = pyqtSignal(bool)