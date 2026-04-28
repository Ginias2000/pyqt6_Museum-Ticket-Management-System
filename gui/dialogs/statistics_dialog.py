"""
Statistics Dialog - Detailed statistics and analytics
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
    QTableWidget, QTableWidgetItem, QLabel,
    QGroupBox, QGridLayout, QHeaderView, QFrame
)
from PyQt6.QtCore import Qt


class StatisticsDialog(QDialog):
    """Detailed statistics dialog"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
        self.load_statistics()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("📊 Statistics Report")
        self.setModal(True)
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
        
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
            QTableWidget {
                background-color: #1e1e2f;
                border: none;
                gridline-color: #2d2d3f;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Statistics & Analytics")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)
        
        # Tab widget
        tabs = QTabWidget()
        
        # Overview tab
        overview_tab = self.create_overview_tab()
        tabs.addTab(overview_tab, "Overview")
        
        # Sales tab
        sales_tab = self.create_sales_tab()
        tabs.addTab(sales_tab, "Sales Analysis")
        
        # Visitors tab
        visitors_tab = self.create_visitors_tab()
        tabs.addTab(visitors_tab, "Visitor Statistics")
        
        layout.addWidget(tabs)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a6cf7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)
    
    def create_overview_tab(self):
        """Create overview statistics tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Stats grid
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color: #181826; border-radius: 12px; padding: 15px;")
        stats_layout = QGridLayout(stats_frame)
        stats_layout.setSpacing(20)
        
        self.stats_labels = {}
        stats_items = [
            ("Total Visitors", "total_visitors", "👥"),
            ("Total Tickets", "total_tickets", "🎫"),
            ("Total Revenue", "total_revenue", "💰"),
            ("Today's Visitors", "today_visitors", "📅"),
            ("Today's Revenue", "today_revenue", "💵"),
            ("Active Visitors", "active_visitors", "🏛️"),
        ]
        
        for i, (label, key, icon) in enumerate(stats_items):
            row, col = i // 2, i % 2
            container = QFrame()
            container_layout = QVBoxLayout(container)
            
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 32px;")
            container_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
            
            value_label = QLabel("—")
            value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4a6cf7;")
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            container_layout.addWidget(value_label)
            
            name_label = QLabel(label)
            name_label.setStyleSheet("color: #a0a0c0;")
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            container_layout.addWidget(name_label)
            
            stats_layout.addWidget(container, row, col)
            self.stats_labels[key] = value_label
        
        layout.addWidget(stats_frame)
        layout.addStretch()
        
        return tab
    
    def create_sales_tab(self):
        """Create sales analysis tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Top selling ticket types
        top_group = QGroupBox("Top Selling Ticket Types")
        top_layout = QVBoxLayout(top_group)
        
        self.top_sales_table = QTableWidget()
        self.top_sales_table.setColumnCount(3)
        self.top_sales_table.setHorizontalHeaderLabels(["Ticket Type", "Sold", "Revenue"])
        self.top_sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        top_layout.addWidget(self.top_sales_table)
        
        layout.addWidget(top_group)
        
        # Hourly breakdown
        hourly_group = QGroupBox("Hourly Sales Breakdown")
        hourly_layout = QVBoxLayout(hourly_group)
        
        self.hourly_table = QTableWidget()
        self.hourly_table.setColumnCount(3)
        self.hourly_table.setHorizontalHeaderLabels(["Hour", "Tickets Sold", "Revenue"])
        self.hourly_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        hourly_layout.addWidget(self.hourly_table)
        
        layout.addWidget(hourly_group)
        
        return tab
    
    def create_visitors_tab(self):
        """Create visitor statistics tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Daily visitor report
        daily_group = QGroupBox("Daily Visitor Statistics")
        daily_layout = QVBoxLayout(daily_group)
        
        self.visitor_stats_table = QTableWidget()
        self.visitor_stats_table.setColumnCount(4)
        self.visitor_stats_table.setHorizontalHeaderLabels(["Date", "Entries", "Exits", "Avg Duration"])
        self.visitor_stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        daily_layout.addWidget(self.visitor_stats_table)
        
        layout.addWidget(daily_group)
        
        return tab
    
    def load_statistics(self):
        """Load all statistics data"""
        try:
            # Load total statistics
            stats = self.db_manager.get_total_statistics()
            
            for key, label in self.stats_labels.items():
                value = stats.get(key, 0)
                if key in ['total_revenue', 'today_revenue']:
                    label.setText(f"¥{value:,.2f}")
                else:
                    label.setText(str(value))
            
            # Load top ticket types
            top_types = self.db_manager.get_top_ticket_types(5)
            self.top_sales_table.setRowCount(len(top_types))
            for i, row in enumerate(top_types):
                self.top_sales_table.setItem(i, 0, QTableWidgetItem(row.get('name', '—')))
                self.top_sales_table.setItem(i, 1, QTableWidgetItem(str(row.get('tickets_sold', 0))))
                self.top_sales_table.setItem(i, 2, QTableWidgetItem(f"¥{row.get('revenue', 0):.2f}"))
            
            # Load hourly breakdown
            import datetime
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            hourly = self.db_manager.get_hourly_sales_breakdown(today)
            self.hourly_table.setRowCount(len(hourly))
            for i, row in enumerate(hourly):
                self.hourly_table.setItem(i, 0, QTableWidgetItem(f"{row.get('hour', '—')}:00"))
                self.hourly_table.setItem(i, 1, QTableWidgetItem(str(row.get('tickets_sold', 0))))
                self.hourly_table.setItem(i, 2, QTableWidgetItem(f"¥{row.get('revenue', 0):.2f}"))
            
        except Exception as e:
            print(f"Error loading statistics: {e}")