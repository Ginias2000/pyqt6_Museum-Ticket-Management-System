"""
Main Window - Professional Museum Management System GUI
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QStackedWidget,
    QLabel, QFrame, QApplication, QPushButton
)
from PyQt6.QtCore import Qt, QTimer, QDateTime, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from gui.styles import MODERN_STYLE
from gui.pages.dashboard_page import DashboardPage
from gui.pages.ticket_sales_page import TicketSalesPage
from gui.pages.visitor_management_page import VisitorManagementPage
from gui.pages.reports_page import ReportsPage
from gui.pages.settings_page import SettingsPage


class NavigationItem(QListWidgetItem):
    """Custom navigation list item"""
    def __init__(self, text: str, icon_emoji: str, page_index: int):
        super().__init__(f"  {icon_emoji}  {text}")
        self.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        self.page_index = page_index
        self.setSizeHint(self.sizeHint())


class MainWindow(QMainWindow):
    """Professional main window for museum management system"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Museum Ticket Management System")
        self.setMinimumSize(1280, 800)
        self.resize(1400, 900)
        
        # Set stylesheet
        self.setStyleSheet(MODERN_STYLE)
        
        # Create central widget
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Right content area
        content_area = self.create_content_area()
        main_layout.addWidget(content_area, stretch=1)
        
    def create_sidebar(self):
        """Create the left navigation sidebar"""
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar")
        sidebar_widget.setFixedWidth(260)
        
        layout = QVBoxLayout(sidebar_widget)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(20)
        
        # Logo area
        logo_label = QLabel("🎨 MUSEUM SYS")
        logo_label.setObjectName("titleLabel")
        logo_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        logo_label.setFont(logo_font)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #2d2d3f; max-height: 1px;")
        layout.addWidget(separator)
        
        # Navigation list
        self.navigation = QListWidget()
        self.navigation.setObjectName("navigation")
        self.navigation.setIconSize(QtCore.QSize(24, 24))
        self.navigation.setSpacing(4)
        
        # Navigation items
        nav_items = [
            ("📊", "Dashboard", 0),
            ("🎫", "Ticket Sales", 1),
            ("👥", "Visitor Management", 2),
            ("📈", "Reports", 3),
            ("⚙️", "Settings", 4),
        ]
        
        for icon, text, index in nav_items:
            item = NavigationItem(text, icon, index)
            self.navigation.addItem(item)
        
        self.navigation.currentRowChanged.connect(self.switch_page)
        layout.addWidget(self.navigation)
        
        # Spacer
        layout.addStretch()
        
        # User info at bottom
        user_widget = QFrame()
        user_widget.setStyleSheet("""
            QFrame {
                background-color: #181826;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        user_layout = QHBoxLayout(user_widget)
        
        avatar = QLabel("👤")
        avatar.setStyleSheet("font-size: 24px;")
        user_layout.addWidget(avatar)
        
        user_info = QVBoxLayout()
        user_name = QLabel("Admin User")
        user_name.setStyleSheet("color: white; font-weight: bold;")
        user_role = QLabel("System Administrator")
        user_role.setStyleSheet("color: #a0a0c0; font-size: 11px;")
        user_info.addWidget(user_name)
        user_info.addWidget(user_role)
        user_layout.addLayout(user_info)
        
        layout.addWidget(user_widget)
        
        return sidebar_widget
    
    def create_content_area(self):
        """Create the main content area with stacked pages"""
        # Top bar
        top_bar = QWidget()
        top_bar.setObjectName("topBar")
        top_bar.setFixedHeight(70)
        
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(30, 0, 30, 0)
        
        # Page title
        self.page_title = QLabel("Dashboard")
        self.page_title.setObjectName("titleLabel")
        page_title_font = QFont("Segoe UI", 24, QFont.Weight.Bold)
        self.page_title.setFont(page_title_font)
        top_layout.addWidget(self.page_title)
        
        top_layout.addStretch()
        
        # Date and time
        self.time_label = QLabel()
        self.time_label.setObjectName("timeLabel")
        time_font = QFont("Segoe UI", 12)
        self.time_label.setFont(time_font)
        top_layout.addWidget(self.time_label)
        
        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        
        # Create pages
        self.dashboard_page = DashboardPage(self.db_manager)
        self.ticket_sales_page = TicketSalesPage(self.db_manager)
        self.visitor_page = VisitorManagementPage(self.db_manager)
        self.reports_page = ReportsPage(self.db_manager)
        self.settings_page = SettingsPage(self.db_manager)
        
        # Add pages
        self.stacked_widget.addWidget(self.dashboard_page)    # index 0
        self.stacked_widget.addWidget(self.ticket_sales_page) # index 1
        self.stacked_widget.addWidget(self.visitor_page)      # index 2
        self.stacked_widget.addWidget(self.reports_page)      # index 3
        self.stacked_widget.addWidget(self.settings_page)     # index 4
        
        # Main content layout
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addWidget(top_bar)
        content_layout.addWidget(self.stacked_widget, stretch=1)
        
        return content_widget
    
    def switch_page(self, index):
        """Switch between pages"""
        if index >= 0:
            self.stacked_widget.setCurrentIndex(index)
            page_names = ["Dashboard", "Ticket Sales", "Visitor Management", "Reports", "Settings"]
            self.page_title.setText(page_names[index])
            
            # Refresh page data when switched
            if index == 0:
                self.dashboard_page.refresh()
            elif index == 1:
                self.ticket_sales_page.refresh()
            elif index == 2:
                self.visitor_page.refresh()
            elif index == 3:
                self.reports_page.refresh()
    
    def setup_timer(self):
        """Setup timer for real-time clock"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second
        self.update_time()
    
    def update_time(self):
        """Update the time display"""
        current_time = QDateTime.currentDateTime()
        self.time_label.setText(current_time.toString("dddd, MMMM d, yyyy  hh:mm:ss AP"))


# Fix missing import
import PyQt6.QtCore as QtCore