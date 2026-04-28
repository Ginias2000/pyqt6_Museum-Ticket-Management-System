"""
Configuration Dialog - System settings dialog
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
    QFormLayout, QSpinBox, QTimeEdit, QLineEdit,
    QPushButton, QMessageBox, QGroupBox, QLabel
)
from PyQt6.QtCore import Qt, QTime


class ConfigDialog(QDialog):
    """System configuration dialog"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
        self.load_config()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("⚙️ System Configuration")
        self.setModal(True)
        self.setMinimumWidth(550)
        self.setMinimumHeight(450)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2f;
            }
            QGroupBox {
                color: #ffffff;
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
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("System Configuration")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)
        
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
                padding: 8px 16px;
                border-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #4a6cf7;
                color: #ffffff;
            }
        """)
        
        # General tab
        general_tab = self.create_general_tab()
        tabs.addTab(general_tab, "General")
        
        # Ticket Types tab
        ticket_tab = self.create_ticket_types_tab()
        tabs.addTab(ticket_tab, "Ticket Types")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2a3a;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        save_btn.clicked.connect(self.save_config)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        layout.addLayout(button_layout)
    
    def create_general_tab(self):
        """Create general settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        form_widget = QGroupBox("Museum Settings")
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Max capacity
        self.capacity_spin = QSpinBox()
        self.capacity_spin.setRange(1, 500)
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
        form_layout.addRow("Ticket Usage Count:", self.usage_spin)
        
        layout.addWidget(form_widget)
        layout.addStretch()
        
        return tab
    
    def create_ticket_types_tab(self):
        """Create ticket types management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info_label = QLabel(
            "Ticket types are managed in the database.\n\n"
            "Current ticket types:\n"
            "• Senior (¥10) - Age 60+\n"
            "• Child (¥5) - Age 3-12\n"
            "• Adult (¥30) - Age 13-59\n"
            "• Student (¥15) - With valid ID\n"
            "• Free (¥0) - Age under 3 or over 80"
        )
        info_label.setStyleSheet("color: #a0a0c0; padding: 20px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        return tab
    
    def load_config(self):
        """Load configuration from database"""
        max_capacity = self.db_manager.get_config_value("max_capacity")
        if max_capacity:
            self.capacity_spin.setValue(int(max_capacity))
        
        start_time = self.db_manager.get_config_value("ticketing_start_time")
        if start_time:
            parts = start_time.split(":")
            self.start_time.setTime(QTime(int(parts[0]), int(parts[1])))
        
        end_time = self.db_manager.get_config_value("ticketing_end_time")
        if end_time:
            parts = end_time.split(":")
            self.end_time.setTime(QTime(int(parts[0]), int(parts[1])))
        
        usage_count = self.db_manager.get_config_value("ticket_usage_count")
        if usage_count:
            self.usage_spin.setValue(int(usage_count))
    
    def save_config(self):
        """Save configuration to database"""
        self.db_manager.set_config_value("max_capacity", str(self.capacity_spin.value()))
        self.db_manager.set_config_value("ticketing_start_time", self.start_time.time().toString("HH:mm"))
        self.db_manager.set_config_value("ticketing_end_time", self.end_time.time().toString("HH:mm"))
        self.db_manager.set_config_value("ticket_usage_count", str(self.usage_spin.value()))
        
        QMessageBox.information(self, "Success", "Configuration saved successfully!")
        self.accept()