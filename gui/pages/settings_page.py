"""
Settings Page - System Configuration
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox,
    QTimeEdit, QGroupBox, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, QTime


class SettingsPage(QWidget):
    """System settings configuration page"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("⚙️ System Settings")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title_label)
        
        # Tab widget
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                background-color: #1e1e2f;
                border-radius: 12px;
            }
            QTabBar::tab {
                background-color: #181826;
                color: #a0a0c0;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #4a6cf7;
                color: #ffffff;
            }
        """)
        
        # General settings tab
        general_tab = self.create_general_tab()
        tabs.addTab(general_tab, "General")
        
        # Ticket types tab
        ticket_types_tab = self.create_ticket_types_tab()
        tabs.addTab(ticket_types_tab, "Ticket Types")
        
        layout.addWidget(tabs)
        
        # Save button
        save_btn = QPushButton("💾 Save All Settings")
        save_btn.setMinimumHeight(45)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
    
    def create_general_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        form_widget = QGroupBox("Museum Configuration")
        form_widget.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #2d2d3f;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px;
            }
        """)
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Max capacity
        self.capacity_spin = QSpinBox()
        self.capacity_spin.setRange(1, 1000)
        self.capacity_spin.setSuffix(" people")
        self.capacity_spin.setStyleSheet("""
            QSpinBox {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
            }
        """)
        form_layout.addRow("Maximum Capacity:", self.capacity_spin)
        
        # Start time
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("HH:mm")
        self.start_time.setStyleSheet("""
            QTimeEdit {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
            }
        """)
        form_layout.addRow("Ticketing Start Time:", self.start_time)
        
        # End time
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm")
        self.end_time.setStyleSheet("""
            QTimeEdit {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
            }
        """)
        form_layout.addRow("Ticketing End Time:", self.end_time)
        
        # Usage count
        self.usage_spin = QSpinBox()
        self.usage_spin.setRange(1, 10)
        self.usage_spin.setSuffix(" times")
        self.usage_spin.setStyleSheet("""
            QSpinBox {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
            }
        """)
        form_layout.addRow("Ticket Usage Count:", self.usage_spin)
        
        layout.addWidget(form_widget)
        layout.addStretch()
        
        return tab
    
    def create_ticket_types_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info_frame = QGroupBox("Current Ticket Types")
        info_frame.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #2d2d3f;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        
        info_text = QLabel(
            "Ticket Types and Pricing:\n\n"
            "• Senior (Age 60+) - ¥10.00\n"
            "• Child (Age 3-12) - ¥5.00\n"
            "• Adult (Age 13-59) - ¥30.00\n"
            "• Student (Valid ID) - ¥15.00\n"
            "• Free (Under 3 or Over 80) - ¥0.00\n\n"
            "Note: To modify ticket types, please contact the system administrator."
        )
        info_text.setStyleSheet("color: #a0a0c0; padding: 15px;")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_frame)
        layout.addStretch()
        
        return tab
    
    def load_settings(self):
        """Load settings from database"""
        try:
            max_capacity = self.db_manager.get_config_value("max_capacity")
            if max_capacity:
                self.capacity_spin.setValue(int(max_capacity))
            
            start_time = self.db_manager.get_config_value("ticketing_start_time")
            if start_time:
                time_parts = start_time.split(":")
                self.start_time.setTime(QTime(int(time_parts[0]), int(time_parts[1])))
            
            end_time = self.db_manager.get_config_value("ticketing_end_time")
            if end_time:
                time_parts = end_time.split(":")
                self.end_time.setTime(QTime(int(time_parts[0]), int(time_parts[1])))
            
            usage_count = self.db_manager.get_config_value("ticket_usage_count")
            if usage_count:
                self.usage_spin.setValue(int(usage_count))
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to database"""
        try:
            self.db_manager.set_config_value("max_capacity", str(self.capacity_spin.value()))
            self.db_manager.set_config_value("ticketing_start_time", self.start_time.time().toString("HH:mm"))
            self.db_manager.set_config_value("ticketing_end_time", self.end_time.time().toString("HH:mm"))
            self.db_manager.set_config_value("ticket_usage_count", str(self.usage_spin.value()))
            
            QMessageBox.information(self, "Success", "Settings saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")