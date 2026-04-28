"""
Reports Page - Analytics and Reports
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QDateEdit, QGroupBox, QHeaderView, QFrame
)
from PyQt6.QtCore import Qt, QDate


class ReportsPage(QWidget):
    """Professional reports and analytics page"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("📈 Reports & Analytics")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title_label)
        
        # Date selector
        date_widget = QFrame()
        date_widget.setStyleSheet("background-color: #181826; border-radius: 12px; padding: 15px;")
        date_layout = QHBoxLayout(date_widget)
        
        date_layout.addWidget(QLabel("Select Date:"))
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        date_layout.addWidget(self.date_edit)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setFixedWidth(100)
        self.refresh_btn.clicked.connect(self.refresh)
        date_layout.addWidget(self.refresh_btn)
        
        date_layout.addStretch()
        layout.addWidget(date_widget)
        
        # Sales report table
        sales_group = QGroupBox("Sales Report")
        sales_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; color: #ffffff; }")
        sales_layout = QVBoxLayout(sales_group)
        
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(4)
        self.sales_table.setHorizontalHeaderLabels(["Ticket Type", "Quantity", "Revenue", "Avg Price"])
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        sales_layout.addWidget(self.sales_table)
        
        layout.addWidget(sales_group)
        
        # Visitor report
        visitor_group = QGroupBox("Visitor Statistics")
        visitor_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; color: #ffffff; }")
        visitor_layout = QGridLayout(visitor_group)
        
        visitor_layout.addWidget(QLabel("Total Entries:"), 0, 0)
        self.total_entries_label = QLabel("—")
        self.total_entries_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4a6cf7;")
        visitor_layout.addWidget(self.total_entries_label, 0, 1)
        
        visitor_layout.addWidget(QLabel("Average Duration:"), 1, 0)
        self.avg_duration_label = QLabel("—")
        self.avg_duration_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #27ae60;")
        visitor_layout.addWidget(self.avg_duration_label, 1, 1)
        
        layout.addWidget(visitor_group)
        
        self.refresh()
    
    def refresh(self):
        """Refresh report data"""
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")
        
        # Load sales report
        sales_data = self.db_manager.get_daily_sales_report(selected_date)
        
        self.sales_table.setRowCount(len(sales_data))
        total_revenue = 0
        total_tickets = 0
        
        for i, row in enumerate(sales_data):
            ticket_type = row.get("ticket_type", "—")
            count = row.get("count", 0)
            revenue = row.get("revenue", 0)
            avg_price = revenue / count if count > 0 else 0
            
            self.sales_table.setItem(i, 0, QTableWidgetItem(ticket_type))
            self.sales_table.setItem(i, 1, QTableWidgetItem(str(count)))
            self.sales_table.setItem(i, 2, QTableWidgetItem(f"¥{revenue:.2f}"))
            self.sales_table.setItem(i, 3, QTableWidgetItem(f"¥{avg_price:.2f}"))
            
            total_tickets += count
            total_revenue += revenue
        
        # Load visitor report
        try:
            visitor_data = self.db_manager.get_daily_visitor_report(selected_date)
            self.total_entries_label.setText(str(visitor_data.get("total_entries", 0)))
            avg_duration = visitor_data.get("average_duration_minutes", 0)
            self.avg_duration_label.setText(f"{avg_duration:.0f} min" if avg_duration else "—")
        except:
            self.total_entries_label.setText("—")
            self.avg_duration_label.setText("—")