"""
Ticket Sale Dialog - Modal dialog for ticket sales
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QSpinBox, QFrame,
    QMessageBox, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from gui.widgets.modern_widgets import ModernLineEdit, ModernButton
from gui.widgets.card_widget import CardWidget


class TicketSaleDialog(QDialog):
    """Professional ticket sale dialog"""
    
    ticket_sold = pyqtSignal(dict)
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.selected_ticket_type = None
        self.setup_ui()
        self.load_ticket_types()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("🎫 Sell Ticket")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2f;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Sell New Ticket")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)
        
        # Visitor information section
        visitor_section = QFrame()
        visitor_section.setStyleSheet("""
            QFrame {
                background-color: #181826;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        visitor_layout = QGridLayout(visitor_section)
        visitor_layout.setSpacing(12)
        
        visitor_layout.addWidget(QLabel("Name:"), 0, 0)
        self.name_input = ModernLineEdit("Enter visitor name")
        visitor_layout.addWidget(self.name_input, 0, 1)
        
        visitor_layout.addWidget(QLabel("ID Number:"), 1, 0)
        self.id_input = ModernLineEdit("Enter ID number")
        visitor_layout.addWidget(self.id_input, 1, 1)
        
        visitor_layout.addWidget(QLabel("Gender:"), 2, 0)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        self.gender_combo.setStyleSheet("""
            QComboBox {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
            }
        """)
        visitor_layout.addWidget(self.gender_combo, 2, 1)
        
        visitor_layout.addWidget(QLabel("Date of Birth:"), 3, 0)
        self.dob_input = ModernLineEdit("YYYY-MM-DD")
        visitor_layout.addWidget(self.dob_input, 3, 1)
        
        layout.addWidget(visitor_section)
        
        # Ticket selection section
        ticket_section = QFrame()
        ticket_section.setStyleSheet("""
            QFrame {
                background-color: #181826;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        ticket_layout = QVBoxLayout(ticket_section)
        
        ticket_layout.addWidget(QLabel("Select Ticket Type:"))
        
        self.ticket_types_layout = QGridLayout()
        self.ticket_types_layout.setSpacing(10)
        ticket_layout.addLayout(self.ticket_types_layout)
        
        # Quantity
        quantity_layout = QHBoxLayout()
        quantity_layout.addWidget(QLabel("Quantity:"))
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(10)
        self.quantity_spin.setStyleSheet("""
            QSpinBox {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
            }
        """)
        quantity_layout.addWidget(self.quantity_spin)
        quantity_layout.addStretch()
        ticket_layout.addLayout(quantity_layout)
        
        layout.addWidget(ticket_section)
        
        # Total and buttons
        total_frame = QFrame()
        total_layout = QHBoxLayout(total_frame)
        total_layout.addWidget(QLabel("Total:"))
        self.total_label = QLabel("¥0.00")
        self.total_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4a6cf7;")
        total_layout.addWidget(self.total_label)
        total_layout.addStretch()
        layout.addWidget(total_frame)
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = ModernButton("Cancel", variant="secondary")
        cancel_btn.clicked.connect(self.reject)
        self.sell_btn = ModernButton("Sell Ticket", variant="success")
        self.sell_btn.setEnabled(False)
        self.sell_btn.clicked.connect(self.sell_ticket)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(self.sell_btn)
        layout.addLayout(button_layout)
    
    def load_ticket_types(self):
        """Load ticket types as buttons"""
        ticket_types = self.db_manager.get_all_ticket_types()
        
        self.ticket_buttons = {}
        row, col = 0, 0
        for tt in ticket_types:
            btn = QPushButton(f"{tt.name}\n¥{tt.price}")
            btn.setMinimumHeight(70)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #252535;
                    border: 1px solid #2d2d3f;
                    border-radius: 8px;
                    color: #ffffff;
                }
                QPushButton:hover {
                    border-color: #4a6cf7;
                }
                QPushButton:checked {
                    background-color: #4a6cf7;
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, t=tt: self.select_ticket_type(t))
            self.ticket_types_layout.addWidget(btn, row, col)
            self.ticket_buttons[tt.id] = btn
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
    
    def select_ticket_type(self, ticket_type):
        """Select a ticket type"""
        # Uncheck all other buttons
        for btn in self.ticket_buttons.values():
            btn.setChecked(False)
        
        self.ticket_buttons[ticket_type.id].setChecked(True)
        self.selected_ticket_type = ticket_type
        self.update_total()
        self.sell_btn.setEnabled(True)
    
    def update_total(self):
        """Update total price display"""
        if self.selected_ticket_type:
            total = self.selected_ticket_type.price * self.quantity_spin.value()
            self.total_label.setText(f"¥{total:.2f}")
    
    def sell_ticket(self):
        """Process ticket sale"""
        if not self.selected_ticket_type:
            QMessageBox.warning(self, "Warning", "Please select a ticket type")
            return
        
        # Validate required fields
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter visitor name")
            return
        
        if not self.id_input.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter ID number")
            return
        
        # Create or get visitor
        from models.visitor import Visitor
        visitor = Visitor(
            id_number=self.id_input.text(),
            name=self.name_input.text(),
            gender=self.gender_combo.currentText(),
            date_of_birth=self.dob_input.text()
        )
        
        # Check if visitor exists
        existing = self.db_manager.get_visitor_by_id_number(visitor.id_number)
        if existing:
            visitor_id = existing.id
        else:
            visitor_id = self.db_manager.create_visitor(visitor)
        
        # Create tickets
        tickets = []
        for _ in range(self.quantity_spin.value()):
            from models.ticket import Ticket
            ticket = Ticket(
                visitor_id=visitor_id,
                ticket_type_id=self.selected_ticket_type.id,
                price=self.selected_ticket_type.price
            )
            ticket_id = self.db_manager.create_ticket(ticket)
            tickets.append(ticket)
        
        # Emit signal
        self.ticket_sold.emit({
            "tickets": tickets,
            "total": self.selected_ticket_type.price * self.quantity_spin.value()
        })
        
        QMessageBox.information(
            self,
            "Success",
            f"✅ Successfully sold {len(tickets)} ticket(s)!\nTotal: ¥{self.selected_ticket_type.price * self.quantity_spin.value():.2f}"
        )
        
        self.accept()