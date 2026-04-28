"""
Visitor Entry Dialog - Modal dialog for visitor entry processing
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from gui.widgets.modern_widgets import ModernLineEdit, ModernButton


class VisitorEntryDialog(QDialog):
    """Dialog for processing visitor entry"""
    
    entry_processed = pyqtSignal(dict)
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("🚪 Visitor Entry")
        self.setModal(True)
        self.setMinimumWidth(450)
        self.setMinimumHeight(300)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2f;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Process Visitor Entry")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)
        
        # Ticket ID input
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #181826;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        
        input_layout.addWidget(QLabel("Scan or Enter Ticket ID:"))
        self.ticket_input = ModernLineEdit("Enter ticket ID...")
        self.ticket_input.returnPressed.connect(self.process_entry)
        input_layout.addWidget(self.ticket_input)
        
        layout.addWidget(input_frame)
        
        # Ticket info display
        self.info_frame = QFrame()
        self.info_frame.setStyleSheet("""
            QFrame {
                background-color: #181826;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        self.info_layout = QVBoxLayout(self.info_frame)
        self.info_layout.addWidget(QLabel("Ticket Information will appear here..."))
        self.info_frame.hide()
        layout.addWidget(self.info_frame)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = ModernButton("Cancel", variant="secondary")
        cancel_btn.clicked.connect(self.reject)
        self.entry_btn = ModernButton("Process Entry", variant="success")
        self.entry_btn.setEnabled(False)
        self.entry_btn.clicked.connect(self.confirm_entry)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(self.entry_btn)
        layout.addLayout(button_layout)
        
        # Connect input change
        self.ticket_input.textChanged.connect(self.on_ticket_input_changed)
    
    def on_ticket_input_changed(self):
        """Handle ticket input change"""
        ticket_id = self.ticket_input.text().strip()
        if len(ticket_id) > 5:  # Minimum length check
            self.validate_ticket(ticket_id)
        else:
            self.info_frame.hide()
            self.entry_btn.setEnabled(False)
            self.status_label.setText("")
    
    def validate_ticket(self, ticket_id: str):
        """Validate ticket and show info"""
        validation = self.db_manager.validate_ticket(ticket_id)
        
        if validation["valid"]:
            ticket = validation["ticket"]
            
            # Clear and update info frame
            self.clear_layout(self.info_layout)
            
            # Add ticket info
            info_grid = QVBoxLayout()
            info_grid.addWidget(QLabel(f"👤 Visitor: {ticket.get('visitor_name', 'N/A')}"))
            info_grid.addWidget(QLabel(f"🎫 Ticket Type: {ticket.get('ticket_type_name', 'N/A')}"))
            info_grid.addWidget(QLabel(f"🔄 Remaining Uses: {ticket.get('remaining_uses', 0)}"))
            info_grid.addWidget(QLabel(f"💰 Price: ¥{ticket.get('price', 0):.2f}"))
            
            self.info_layout.addLayout(info_grid)
            self.info_frame.show()
            self.entry_btn.setEnabled(True)
            self.status_label.setStyleSheet("color: #27ae60;")
            self.status_label.setText("✅ Ticket is valid. Click 'Process Entry' to admit visitor.")
            self.validated_ticket = ticket
        else:
            self.info_frame.hide()
            self.entry_btn.setEnabled(False)
            self.status_label.setStyleSheet("color: #e74c3c;")
            self.status_label.setText(f"❌ {validation['reason']}")
            self.validated_ticket = None
    
    def confirm_entry(self):
        """Confirm and process entry"""
        if not hasattr(self, 'validated_ticket') or not self.validated_ticket:
            return
        
        # Check capacity
        active_count = self.db_manager.get_active_visits_count()
        max_capacity = int(self.db_manager.get_config_value("max_capacity") or "10")
        
        if active_count >= max_capacity:
            QMessageBox.warning(self, "Entry Denied", "Museum is at maximum capacity!")
            return
        
        # Process entry
        success = self.db_manager.record_entry(self.validated_ticket["id"])
        
        if success:
            self.entry_processed.emit(self.validated_ticket)
            QMessageBox.information(
                self,
                "Entry Granted",
                f"✅ Welcome {self.validated_ticket['visitor_name']}!\nEnjoy your visit!"
            )
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to process entry")
    
    def clear_layout(self, layout):
        """Clear all widgets from layout"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())