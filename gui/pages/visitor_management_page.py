"""
Visitor Management Page - Entry and exit control
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QGroupBox, QLineEdit, QMessageBox, QFrame, QHeaderView
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

import datetime


class VisitorManagementPage(QWidget):
    """Professional visitor management interface for entry and exit control"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        
    def setup_ui(self):
        """Setup visitor management UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("👥 Visitor Management")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title_label)
        
        # Status bar
        status_widget = QFrame()
        status_widget.setStyleSheet("""
            QFrame {
                background-color: #181826;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        status_layout = QHBoxLayout(status_widget)
        
        self.capacity_label = QLabel("📊 Capacity: 0 / 10")
        self.capacity_label.setStyleSheet("font-size: 14px; color: #ffffff;")
        status_layout.addWidget(self.capacity_label)
        
        status_layout.addStretch()
        
        self.active_count_label = QLabel("👤 Active Visitors: 0")
        self.active_count_label.setStyleSheet("font-size: 14px; color: #4a6cf7; font-weight: bold;")
        status_layout.addWidget(self.active_count_label)
        
        layout.addWidget(status_widget)
        
        # Two-column layout
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        
        # Left: Entry panel
        left_panel = self.create_entry_panel()
        main_layout.addWidget(left_panel, stretch=1)
        
        # Right: Exit panel and active visitors
        right_panel = self.create_exit_panel()
        main_layout.addWidget(right_panel, stretch=2)
        
        layout.addLayout(main_layout)
        
    def create_entry_panel(self):
        """Create entry management panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        entry_group = QGroupBox("🚪 Visitor Entry")
        entry_group.setStyleSheet("""
            QGroupBox { font-weight: bold; font-size: 14px; color: #ffffff; }
        """)
        entry_layout = QVBoxLayout(entry_group)
        
        # Ticket ID input
        entry_layout.addWidget(QLabel("Ticket ID:"))
        self.ticket_id_input = QLineEdit()
        self.ticket_id_input.setPlaceholderText("Enter or scan ticket ID...")
        self.ticket_id_input.returnPressed.connect(self.process_entry)
        entry_layout.addWidget(self.ticket_id_input)
        
        # Process button
        self.entry_btn = QPushButton("✅ Process Entry")
        self.entry_btn.setMinimumHeight(45)
        self.entry_btn.setProperty("class", "btn-success")
        self.entry_btn.clicked.connect(self.process_entry)
        entry_layout.addWidget(self.entry_btn)
        
        layout.addWidget(entry_group)
        
        # Ticket info display
        info_group = QGroupBox("📋 Ticket Information")
        info_group.setStyleSheet("""
            QGroupBox { font-weight: bold; font-size: 14px; color: #ffffff; }
        """)
        info_layout = QGridLayout(info_group)
        
        info_layout.addWidget(QLabel("Visitor:"), 0, 0)
        self.ticket_visitor_label = QLabel("—")
        self.ticket_visitor_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        info_layout.addWidget(self.ticket_visitor_label, 0, 1)
        
        info_layout.addWidget(QLabel("Ticket Type:"), 1, 0)
        self.ticket_type_label = QLabel("—")
        info_layout.addWidget(self.ticket_type_label, 1, 1)
        
        info_layout.addWidget(QLabel("Remaining Uses:"), 2, 0)
        self.remaining_uses_label = QLabel("—")
        info_layout.addWidget(self.remaining_uses_label, 2, 1)
        
        info_layout.addWidget(QLabel("Status:"), 3, 0)
        self.ticket_status_label = QLabel("—")
        info_layout.addWidget(self.ticket_status_label, 3, 1)
        
        layout.addWidget(info_group)
        
        layout.addStretch()
        
        return panel
    
    def create_exit_panel(self):
        """Create exit management panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        exit_group = QGroupBox("🚪 Visitor Exit")
        exit_group.setStyleSheet("""
            QGroupBox { font-weight: bold; font-size: 14px; color: #ffffff; }
        """)
        exit_layout = QVBoxLayout(exit_group)
        
        # Active visitors table
        self.active_visitors_table = QTableWidget()
        self.active_visitors_table.setColumnCount(4)
        self.active_visitors_table.setHorizontalHeaderLabels([
            "Ticket ID", "Visitor Name", "Entry Time", "Action"
        ])
        self.active_visitors_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.active_visitors_table.setAlternatingRowColors(True)
        self.active_visitors_table.setMinimumHeight(300)
        exit_layout.addWidget(self.active_visitors_table)
        
        # Exit with ticket ID
        exit_id_layout = QHBoxLayout()
        exit_id_layout.addWidget(QLabel("Or enter Ticket ID:"))
        self.exit_ticket_input = QLineEdit()
        self.exit_ticket_input.setPlaceholderText("Enter ticket ID to exit...")
        self.exit_ticket_input.returnPressed.connect(self.process_exit_by_id)
        exit_id_layout.addWidget(self.exit_ticket_input)
        
        self.exit_btn = QPushButton("Process Exit")
        self.exit_btn.setProperty("class", "btn-secondary")
        self.exit_btn.clicked.connect(self.process_exit_by_id)
        exit_id_layout.addWidget(self.exit_btn)
        
        exit_layout.addLayout(exit_id_layout)
        
        layout.addWidget(exit_group)
        
        return panel
    
    def refresh(self):
        """Refresh all data"""
        self.update_capacity_info()
        self.load_active_visitors()

    # Add this method to the VisitorManagementPage class in visitor_management_page.py

    def process_exit_by_ticket_id(self, ticket_id: str):
        """Process exit by ticket ID"""
        success = self.db_manager.record_exit(int(ticket_id))
        
        if success:
            QMessageBox.information(self, "Exit Processed", "Visitor has exited successfully")
            self.refresh()
        else:
            QMessageBox.critical(self, "Error", "Failed to process exit")
    
    def update_capacity_info(self):
        """Update capacity display"""
        active_count = self.db_manager.get_active_visits_count()
        max_capacity = int(self.db_manager.get_config_value("max_capacity") or "10")
        
        self.active_count_label.setText(f"👤 Active Visitors: {active_count}")
        self.capacity_label.setText(f"📊 Capacity: {active_count} / {max_capacity}")
        
        # Color coding based on capacity
        percentage = active_count / max_capacity if max_capacity > 0 else 0
        if percentage >= 0.9:
            self.capacity_label.setStyleSheet("font-size: 14px; color: #e74c3c;")
        elif percentage >= 0.7:
            self.capacity_label.setStyleSheet("font-size: 14px; color: #f39c12;")
        else:
            self.capacity_label.setStyleSheet("font-size: 14px; color: #ffffff;")
    
    def load_active_visitors(self):
        """Load list of active visitors"""
        active_visitors = self.db_manager.get_active_visitors()
        
        self.active_visitors_table.setRowCount(len(active_visitors))
        
        for i, visitor in enumerate(active_visitors):
            # Store ticket_id for the action button
            ticket_id = visitor.get("ticket_id", "")
            
            self.active_visitors_table.setItem(i, 0, QTableWidgetItem(ticket_id))
            self.active_visitors_table.setItem(i, 1, QTableWidgetItem(visitor.get("name", "—")))
            self.active_visitors_table.setItem(i, 2, QTableWidgetItem(visitor.get("entry_time", "—")))
            
            # Exit button
            exit_btn = QPushButton("Exit")
            exit_btn.setProperty("class", "btn-secondary")
            exit_btn.setFixedWidth(60)
            exit_btn.clicked.connect(lambda checked, tid=ticket_id: self.process_exit(tid))
            self.active_visitors_table.setCellWidget(i, 3, exit_btn)
    
    def process_entry(self):
        """Process visitor entry"""
        ticket_id = self.ticket_id_input.text().strip()
        
        if not ticket_id:
            QMessageBox.warning(self, "Warning", "Please enter a ticket ID")
            return
        
        # Validate ticket
        validation = self.db_manager.validate_ticket(ticket_id)
        
        if not validation["valid"]:
            QMessageBox.warning(self, "Entry Denied", validation["reason"])
            return
        
        ticket_data = validation["ticket"]
        
        # Check capacity
        active_count = self.db_manager.get_active_visits_count()
        max_capacity = int(self.db_manager.get_config_value("max_capacity") or "10")
        
        if active_count >= max_capacity:
            QMessageBox.warning(self, "Entry Denied", "Museum is at maximum capacity!")
            return
        
        # Record entry
        success = self.db_manager.record_entry(ticket_data["id"])
        
        if success:
            QMessageBox.information(
                self,
                "Entry Granted",
                f"✅ Welcome {ticket_data['visitor_name']}!\n"
                f"Ticket: {ticket_id}\n"
                f"Remaining uses: {ticket_data['remaining_uses'] - 1}"
            )
            self.ticket_id_input.clear()
            self.clear_ticket_info()
            self.refresh()
        else:
            QMessageBox.critical(self, "Error", "Failed to process entry")
    
    def process_exit(self, ticket_id: str):
        """Process visitor exit"""
        confirm = QMessageBox.question(
            self,
            "Confirm Exit",
            f"Process exit for ticket {ticket_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            success = self.db_manager.record_exit(ticket_id)
            
            if success:
                QMessageBox.information(self, "Exit Processed", "Visitor has exited successfully")
                self.refresh()
            else:
                QMessageBox.critical(self, "Error", "Failed to process exit")
    
    def process_exit_by_id(self):
        """Process exit by entered ticket ID"""
        ticket_id = self.exit_ticket_input.text().strip()
        
        if not ticket_id:
            QMessageBox.warning(self, "Warning", "Please enter a ticket ID")
            return
        
        self.process_exit(ticket_id)
        self.exit_ticket_input.clear()
    
    def clear_ticket_info(self):
        """Clear ticket info display"""
        self.ticket_visitor_label.setText("—")
        self.ticket_type_label.setText("—")
        self.remaining_uses_label.setText("—")
        self.ticket_status_label.setText("—")