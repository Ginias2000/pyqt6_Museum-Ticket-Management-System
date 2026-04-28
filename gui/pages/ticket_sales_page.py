"""
Ticket Sales Page - Professional ticket sales interface
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QGroupBox, QLineEdit, QSpinBox, QComboBox,
    QMessageBox, QFrame, QHeaderView, QDialog, QFormLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

import datetime
import random


class ManualIDEntryDialog(QDialog):
    """Dialog for manual ID card entry"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manual ID Card Entry")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2f;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit, QComboBox {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #4a6cf7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #5d7ef8;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        title = QLabel("📇 Manual ID Card Entry")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")
        form_layout.addRow("Full Name:", self.name_input)
        
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("18-digit ID number")
        form_layout.addRow("ID Number:", self.id_input)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        form_layout.addRow("Gender:", self.gender_combo)
        
        self.dob_input = QLineEdit()
        self.dob_input.setPlaceholderText("YYYY-MM-DD")
        form_layout.addRow("Date of Birth:", self.dob_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton("Save & Continue")
        save_btn.clicked.connect(self.accept)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
    
    def get_visitor_data(self):
        """Get entered visitor data"""
        return {
            "name": self.name_input.text(),
            "id_number": self.id_input.text(),
            "gender": self.gender_combo.currentText(),
            "date_of_birth": self.dob_input.text()
        }


class IDCardDisplay(QFrame):
    """Custom widget to display ID card information"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(160)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2d2d4a, stop:1 #252535);
                border-radius: 12px;
                border: 1px solid #4a6cf7;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        
        # Header
        header = QLabel("🪪 ID CARD INFORMATION")
        header.setStyleSheet("color: #4a6cf7; font-size: 10px; font-weight: bold; letter-spacing: 2px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #2d2d3f; max-height: 1px;")
        layout.addWidget(sep)
        
        # Content grid
        content_layout = QGridLayout()
        content_layout.setSpacing(8)
        
        # Icon placeholder
        self.icon_label = QLabel("👤")
        self.icon_label.setStyleSheet("font-size: 36px; background-color: #4a6cf720; border-radius: 30px; padding: 8px;")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setFixedSize(60, 60)
        content_layout.addWidget(self.icon_label, 0, 0, 3, 1)
        
        # Labels
        self.name_label = QLabel("—")
        self.name_label.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold;")
        content_layout.addWidget(self.name_label, 0, 1)
        
        self.id_label = QLabel("—")
        self.id_label.setStyleSheet("color: #a0a0c0; font-size: 11px;")
        content_layout.addWidget(self.id_label, 1, 1)
        
        self.dob_label = QLabel("—")
        self.dob_label.setStyleSheet("color: #a0a0c0; font-size: 11px;")
        content_layout.addWidget(self.dob_label, 2, 1)
        
        layout.addLayout(content_layout)
        
        # Status badge
        self.status_badge = QLabel("● NOT READ")
        self.status_badge.setStyleSheet("color: #e74c3c; font-size: 9px; font-weight: bold;")
        self.status_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_badge)
        
        self.visitor_data = None
    
    def update_display(self, visitor_data):
        """Update the ID card display"""
        if visitor_data:
            self.visitor_data = visitor_data
            self.name_label.setText(visitor_data.get("name", "—"))
            self.id_label.setText(visitor_data.get("id_number", "—"))
            
            dob = visitor_data.get("date_of_birth", "")
            if dob:
                try:
                    birth_date = datetime.datetime.strptime(dob, "%Y-%m-%d")
                    age = datetime.date.today().year - birth_date.year
                    self.dob_label.setText(f"DOB: {dob} (Age: {age})")
                except:
                    self.dob_label.setText(f"DOB: {dob}")
            else:
                self.dob_label.setText("DOB: —")
            
            self.status_badge.setText("● READY FOR SALE")
            self.status_badge.setStyleSheet("color: #27ae60; font-size: 9px; font-weight: bold;")
        else:
            self.name_label.setText("—")
            self.id_label.setText("—")
            self.dob_label.setText("—")
            self.status_badge.setText("● NOT READ")
            self.status_badge.setStyleSheet("color: #e74c3c; font-size: 9px; font-weight: bold;")
            self.visitor_data = None
    
    def clear_display(self):
        """Clear the display"""
        self.update_display(None)


class TicketSalesPage(QWidget):
    """Professional ticket sales interface"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.current_cart = []
        self.selected_ticket_name = None
        self.selected_ticket_price = None
        self.current_visitor = None
        self.ticket_buttons = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup ticket sales UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 15, 25, 25)
        layout.setSpacing(15)
        
        # Title
        title_label = QLabel("🎫 Ticket Sales")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title_label)
        
        # Two-column layout
        main_layout = QHBoxLayout()
        main_layout.setSpacing(15)
        
        # Left: Visitor Info & Ticket Selection
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, stretch=3)
        
        # Right: Cart & Checkout
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, stretch=2)
        
        layout.addLayout(main_layout)
        
        # Load ticket types after UI is created
        self.load_ticket_types()
        
    def create_left_panel(self):
        """Create left panel with visitor info and ticket selection"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(12)
        
        # ID Card Reader Section
        card_group = QGroupBox("📇 ID Card Reader")
        card_group.setStyleSheet("""
            QGroupBox { font-weight: bold; font-size: 13px; color: #ffffff; 
                        border: 1px solid #2d2d3f; border-radius: 10px; 
                        margin-top: 10px; padding-top: 6px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 6px; }
        """)
        card_layout = QVBoxLayout(card_group)
        card_layout.setSpacing(10)
        
        # ID Card Display
        self.id_card_display = IDCardDisplay()
        card_layout.addWidget(self.id_card_display)
        
        # Button row - smaller buttons
        button_row = QHBoxLayout()
        button_row.setSpacing(8)
        
        self.read_card_btn = QPushButton("🔄 Read Card")
        self.read_card_btn.setMinimumHeight(32)
        self.read_card_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a6cf7;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #5d7ef8;
            }
        """)
        self.read_card_btn.clicked.connect(self.read_id_card)
        button_row.addWidget(self.read_card_btn)
        
        self.manual_entry_btn = QPushButton("✏️ Manual")
        self.manual_entry_btn.setMinimumHeight(32)
        self.manual_entry_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2a3a;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #353548;
            }
        """)
        self.manual_entry_btn.clicked.connect(self.manual_id_entry)
        button_row.addWidget(self.manual_entry_btn)
        
        self.clear_card_btn = QPushButton("🗑️ Clear")
        self.clear_card_btn.setMinimumHeight(32)
        self.clear_card_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2a3a;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #353548;
            }
        """)
        self.clear_card_btn.clicked.connect(self.clear_id_card)
        button_row.addWidget(self.clear_card_btn)
        
        card_layout.addLayout(button_row)
        
        layout.addWidget(card_group)
        
        # Ticket selection - COMPACT VERSION
        ticket_group = QGroupBox("🎟️ Select Ticket Type")
        ticket_group.setStyleSheet("""
            QGroupBox { font-weight: bold; font-size: 13px; color: #ffffff; 
                        border: 1px solid #2d2d3f; border-radius: 10px; 
                        margin-top: 10px; padding-top: 6px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 6px; }
        """)
        ticket_layout = QVBoxLayout(ticket_group)
        ticket_layout.setSpacing(8)
        
        # Ticket types grid - COMPACT BUTTONS
        self.ticket_buttons_layout = QGridLayout()
        self.ticket_buttons_layout.setSpacing(8)
        ticket_layout.addLayout(self.ticket_buttons_layout)
        
        # Suggested ticket info
        self.suggested_info = QLabel("💡 Select a ticket type")
        self.suggested_info.setStyleSheet("color: #a0a0c0; font-size: 10px; padding: 4px;")
        ticket_layout.addWidget(self.suggested_info)
        
        # Quantity selector - COMPACT
        quantity_layout = QHBoxLayout()
        quantity_layout.setSpacing(10)
        qty_label = QLabel("Qty:")
        qty_label.setStyleSheet("color: #ffffff; font-size: 12px;")
        quantity_layout.addWidget(qty_label)
        
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(10)
        self.quantity_spin.setValue(1)
        self.quantity_spin.setFixedWidth(60)
        self.quantity_spin.setStyleSheet("""
            QSpinBox {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 6px;
                padding: 4px;
                color: #ffffff;
                font-size: 12px;
            }
        """)
        quantity_layout.addWidget(self.quantity_spin)
        quantity_layout.addStretch()
        ticket_layout.addLayout(quantity_layout)
        
        # Add to cart button - COMPACT
        self.add_to_cart_btn = QPushButton("➕ Add to Cart")
        self.add_to_cart_btn.setMinimumHeight(36)
        self.add_to_cart_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.add_to_cart_btn.clicked.connect(self.add_to_cart)
        ticket_layout.addWidget(self.add_to_cart_btn)
        
        layout.addWidget(ticket_group)
        
        # Payment methods - COMPACT
        payment_group = QGroupBox("💳 Payment")
        payment_group.setStyleSheet("""
            QGroupBox { font-weight: bold; font-size: 13px; color: #ffffff; 
                        border: 1px solid #2d2d3f; border-radius: 10px; 
                        margin-top: 10px; padding-top: 6px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 6px; }
        """)
        payment_layout = QHBoxLayout(payment_group)
        
        payment_methods = ["Cash", "Card", "WeChat", "Alipay"]
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(payment_methods)
        self.payment_combo.setFixedHeight(32)
        self.payment_combo.setStyleSheet("""
            QComboBox {
                background-color: #1e1e2f;
                border: 1px solid #2d2d3f;
                border-radius: 6px;
                padding: 6px;
                color: #ffffff;
                font-size: 12px;
            }
        """)
        payment_layout.addWidget(self.payment_combo)
        
        layout.addWidget(payment_group)
        
        layout.addStretch()
        
        return panel
    
    def create_right_panel(self):
        """Create right panel with cart and checkout"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(12)
        
        # Cart header
        cart_header = QLabel("🛒 Shopping Cart")
        cart_header.setStyleSheet("font-size: 15px; font-weight: bold; color: #ffffff;")
        layout.addWidget(cart_header)
        
        # Cart table
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(4)
        self.cart_table.setHorizontalHeaderLabels(["Type", "Price", "Qty", "Subtotal"])
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.cart_table.setAlternatingRowColors(True)
        self.cart_table.setMinimumHeight(180)
        self.cart_table.setMaximumHeight(250)
        self.cart_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e2f;
                alternate-background-color: #252535;
                gridline-color: #2d2d3f;
                font-size: 11px;
            }
            QTableWidget::item {
                color: #ffffff;
                padding: 6px;
            }
            QHeaderView::section {
                padding: 6px;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.cart_table)
        
        # Cart total
        total_widget = QFrame()
        total_widget.setStyleSheet("""
            QFrame {
                background-color: #181826;
                border-radius: 10px;
                padding: 12px;
            }
        """)
        total_layout = QHBoxLayout(total_widget)
        total_layout.addStretch()
        total_layout.addWidget(QLabel("Total:"))
        self.total_label = QLabel("¥0.00")
        self.total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #4a6cf7;")
        total_layout.addWidget(self.total_label)
        layout.addWidget(total_widget)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.clear_cart_btn = QPushButton("Clear")
        self.clear_cart_btn.setMinimumHeight(36)
        self.clear_cart_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.clear_cart_btn.clicked.connect(self.clear_cart)
        button_layout.addWidget(self.clear_cart_btn)
        
        self.checkout_btn = QPushButton("💰 Pay Now")
        self.checkout_btn.setMinimumHeight(36)
        self.checkout_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.checkout_btn.clicked.connect(self.process_payment)
        button_layout.addWidget(self.checkout_btn)
        
        layout.addLayout(button_layout)
        
        # Recent sales
        recent_label = QLabel("📋 Recent Sales")
        recent_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #ffffff; margin-top: 8px;")
        layout.addWidget(recent_label)
        
        self.recent_table = QTableWidget()
        self.recent_table.setColumnCount(3)
        self.recent_table.setHorizontalHeaderLabels(["Ticket ID", "Type", "Time"])
        self.recent_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.recent_table.setMaximumHeight(140)
        self.recent_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e2f;
                gridline-color: #2d2d3f;
                font-size: 10px;
            }
            QTableWidget::item {
                color: #ffffff;
                padding: 5px;
            }
        """)
        layout.addWidget(self.recent_table)
        
        return panel
    
    def refresh(self):
        """Refresh ticket types and recent sales"""
        self.load_ticket_types()
        self.load_recent_sales()
    
    def load_ticket_types(self):
        """Load ticket types from database - COMPACT BUTTONS"""
        # Clear existing buttons
        for i in reversed(range(self.ticket_buttons_layout.count())):
            widget = self.ticket_buttons_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Load from database
        ticket_types = self.db_manager.get_all_ticket_types()
        
        self.ticket_buttons = {}
        row, col = 0, 0
        
        # Compact button style
        for tt in ticket_types:
            btn = QPushButton(f"{tt.name}\n¥{tt.price}")
            btn.setMinimumHeight(55)
            btn.setMaximumWidth(100)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #252535;
                    border: 1px solid #2d2d3f;
                    border-radius: 8px;
                    color: #ffffff;
                    font-size: 11px;
                    padding: 6px;
                }
                QPushButton:hover {
                    border-color: #4a6cf7;
                    background-color: #2a2a3f;
                }
            """)
            btn.setProperty("ticket_type", tt.name)
            btn.clicked.connect(lambda checked, n=tt.name, p=tt.price: self.select_ticket_type(n, p))
            self.ticket_buttons_layout.addWidget(btn, row, col)
            self.ticket_buttons[tt.name] = {"price": tt.price, "button": btn}
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
    
    def select_ticket_type(self, name: str, price: float):
        """Select a ticket type"""
        self.selected_ticket_name = name
        self.selected_ticket_price = price
        
        # Highlight selected button
        for btn_name, data in self.ticket_buttons.items():
            data["button"].setStyleSheet("""
                QPushButton {
                    background-color: #252535;
                    border: 1px solid #2d2d3f;
                    border-radius: 8px;
                    color: #ffffff;
                    font-size: 11px;
                    padding: 6px;
                }
            """)
        
        if name in self.ticket_buttons:
            self.ticket_buttons[name]["button"].setStyleSheet("""
                QPushButton {
                    background-color: #4a6cf7;
                    border: 2px solid #4a6cf7;
                    border-radius: 8px;
                    color: #ffffff;
                    font-size: 11px;
                    padding: 6px;
                }
            """)
            self.suggested_info.setText(f"✅ Selected: {name} - ¥{price}")
    
    def read_id_card(self):
        """Simulate reading an ID card"""
        try:
            # Generate random Chinese ID card data
            id_number = self.generate_id_number()
            name = self.generate_chinese_name()
            gender = "Male" if int(id_number[16]) % 2 == 1 else "Female"
            
            birth_date_str = id_number[6:14]
            birth_year = int(birth_date_str[0:4])
            birth_month = int(birth_date_str[4:6])
            birth_day = int(birth_date_str[6:8])
            
            birth_date = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
            
            today = datetime.date.today()
            age = today.year - birth_year
            if (today.month, today.day) < (birth_month, birth_day):
                age -= 1
            
            # Determine suggested ticket type
            if age < 12:
                suggested = "Child"
            elif age >= 60:
                suggested = "Senior"
            elif 12 <= age < 18:
                suggested = "Student"
            else:
                suggested = "Adult"
            
            # Store visitor info
            self.current_visitor = {
                "id_number": id_number,
                "name": name,
                "gender": gender,
                "date_of_birth": birth_date,
                "age": age,
                "suggested_ticket": suggested
            }
            
            # Update ID card display
            self.id_card_display.update_display(self.current_visitor)
            
            # Auto-select suggested ticket if available
            if suggested in self.ticket_buttons:
                self.select_ticket_type(suggested, self.ticket_buttons[suggested]["price"])
                self.suggested_info.setText(f"💡 Suggested: {suggested} (Age: {age})")
            else:
                self.suggested_info.setText(f"💡 Age {age} - Select a ticket")
            
            # Show success message
            QMessageBox.information(self, "ID Card Read", 
                f"✅ ID Card Read Successfully!\n\n"
                f"📇 Name: {name}\n"
                f"🆔 ID: {id_number}\n"
                f"🎂 Age: {age}\n"
                f"🎫 Suggested: {suggested} Ticket")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to read ID card: {e}")
    
    def manual_id_entry(self):
        """Open manual ID entry dialog"""
        dialog = ManualIDEntryDialog(self)
        if dialog.exec():
            visitor_data = dialog.get_visitor_data()
            
            if not visitor_data["name"] or not visitor_data["id_number"]:
                QMessageBox.warning(self, "Error", "Please fill in all required fields")
                return
            
            # Calculate age from date of birth
            age = 0
            suggested = "Adult"
            try:
                if visitor_data["date_of_birth"]:
                    birth_date = datetime.datetime.strptime(visitor_data["date_of_birth"], "%Y-%m-%d")
                    today = datetime.date.today()
                    age = today.year - birth_date.year
                    if (today.month, today.day) < (birth_date.month, birth_date.day):
                        age -= 1
                    
                    if age < 12:
                        suggested = "Child"
                    elif age >= 60:
                        suggested = "Senior"
                    elif 12 <= age < 18:
                        suggested = "Student"
            except:
                pass
            
            self.current_visitor = {
                "id_number": visitor_data["id_number"],
                "name": visitor_data["name"],
                "gender": visitor_data["gender"],
                "date_of_birth": visitor_data["date_of_birth"],
                "age": age,
                "suggested_ticket": suggested
            }
            
            # Update display
            self.id_card_display.update_display(self.current_visitor)
            
            # Auto-select suggested
            if suggested in self.ticket_buttons:
                self.select_ticket_type(suggested, self.ticket_buttons[suggested]["price"])
            
            QMessageBox.information(self, "Success", "Visitor information added successfully!")
    
    def clear_id_card(self):
        """Clear the ID card display"""
        self.current_visitor = None
        self.id_card_display.clear_display()
        self.selected_ticket_name = None
        self.selected_ticket_price = None
        self.suggested_info.setText("💡 Select a ticket type")
        
        # Reset button highlights
        for btn_name, data in self.ticket_buttons.items():
            data["button"].setStyleSheet("""
                QPushButton {
                    background-color: #252535;
                    border: 1px solid #2d2d3f;
                    border-radius: 8px;
                    color: #ffffff;
                    font-size: 11px;
                    padding: 6px;
                }
            """)
    
    def generate_id_number(self) -> str:
        """Generate a simulated Chinese ID number"""
        area = "110101"
        year = random.randint(1950, 2015)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        birth = f"{year}{month:02d}{day:02d}"
        seq = f"{random.randint(1, 999):03d}"
        check = random.randint(0, 9)
        return f"{area}{birth}{seq}{check}"
    
    def generate_chinese_name(self) -> str:
        """Generate a random Chinese name"""
        surnames = ["王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴"]
        given_names = ["伟", "芳", "娜", "敏", "静", "涛", "军", "强", "鹏", "宇"]
        return random.choice(surnames) + random.choice(given_names)
    
    def add_to_cart(self):
        """Add selected ticket to cart"""
        if not self.current_visitor:
            QMessageBox.warning(self, "Warning", "Please read an ID card first")
            return
        
        if not self.selected_ticket_name or self.selected_ticket_name not in self.ticket_buttons:
            QMessageBox.warning(self, "Warning", "Please select a ticket type first")
            return
        
        quantity = self.quantity_spin.value()
        price = self.ticket_buttons[self.selected_ticket_name]["price"]
        subtotal = price * quantity
        
        cart_item = {
            "ticket_type": self.selected_ticket_name,
            "price": price,
            "quantity": quantity,
            "subtotal": subtotal
        }
        
        # Check if same type already in cart
        found = False
        for item in self.current_cart:
            if item["ticket_type"] == cart_item["ticket_type"]:
                item["quantity"] += quantity
                item["subtotal"] += subtotal
                found = True
                break
        
        if not found:
            self.current_cart.append(cart_item)
        
        self.update_cart_display()
        
        QMessageBox.information(self, "Added to Cart", 
            f"Added {quantity}x {self.selected_ticket_name} ticket(s)\nSubtotal: ¥{subtotal:.2f}")
    
    def update_cart_display(self):
        """Update the cart table display"""
        self.cart_table.setRowCount(len(self.current_cart))
        
        total = 0
        for i, item in enumerate(self.current_cart):
            self.cart_table.setItem(i, 0, QTableWidgetItem(item["ticket_type"]))
            self.cart_table.setItem(i, 1, QTableWidgetItem(f"¥{item['price']:.2f}"))
            self.cart_table.setItem(i, 2, QTableWidgetItem(str(item["quantity"])))
            self.cart_table.setItem(i, 3, QTableWidgetItem(f"¥{item['subtotal']:.2f}"))
            total += item["subtotal"]
        
        self.total_label.setText(f"¥{total:.2f}")
    
    def clear_cart(self):
        """Clear the shopping cart"""
        self.current_cart = []
        self.update_cart_display()
    
    def process_payment(self):
        """Process payment and generate tickets"""
        if not self.current_visitor:
            QMessageBox.warning(self, "Warning", "Please read an ID card first")
            return
        
        if not self.current_cart:
            QMessageBox.warning(self, "Warning", "Cart is empty")
            return
        
        # Check if visitor already exists
        visitor = self.db_manager.get_visitor_by_id_number(self.current_visitor["id_number"])
        
        if not visitor:
            from models.visitor import Visitor
            visitor = Visitor(
                id_number=self.current_visitor["id_number"],
                name=self.current_visitor["name"],
                gender=self.current_visitor["gender"],
                date_of_birth=self.current_visitor["date_of_birth"]
            )
            visitor_id = self.db_manager.create_visitor(visitor)
        else:
            visitor_id = visitor.id
        
        # Create tickets
        tickets_created = []
        for item in self.current_cart:
            ticket_type = self.db_manager.get_ticket_type_by_name(item["ticket_type"])
            
            if ticket_type:
                for _ in range(item["quantity"]):
                    from models.ticket import Ticket
                    ticket = Ticket(
                        visitor_id=visitor_id,
                        ticket_type_id=ticket_type.id,
                        price=ticket_type.price,
                        sale_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    ticket_id = self.db_manager.create_ticket(ticket)
                    tickets_created.append(ticket)
        
        # Show success message
        total_amount = sum(item["subtotal"] for item in self.current_cart)
        QMessageBox.information(
            self, 
            "Payment Successful", 
            f"✅ Purchased {len(tickets_created)} tickets!\n"
            f"👤 {self.current_visitor['name']}\n"
            f"💰 ¥{total_amount:.2f}\n"
            f"💳 {self.payment_combo.currentText()}"
        )
        
        # Clear cart and reset
        self.clear_cart()
        self.clear_id_card()
        self.load_recent_sales()
    
    def load_recent_sales(self):
        """Load recent sales into the table"""
        try:
            self.recent_table.setRowCount(0)
            self.recent_table.setRowCount(3)
            now = datetime.datetime.now()
            for i in range(3):
                self.recent_table.setItem(i, 0, QTableWidgetItem(f"TKT{now.strftime('%H%M%S')}{i:03d}"))
                self.recent_table.setItem(i, 1, QTableWidgetItem(["Adult", "Child", "Senior"][i]))
                self.recent_table.setItem(i, 2, QTableWidgetItem(now.strftime("%H:%M:%S")))
        except Exception as e:
            print(f"Error loading recent sales: {e}")