"""
Museum Ticket Management System
Main Application Entry Point
Author: [Your Name]
Student ID: [Your Student ID]
Date: 2026-04-28
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

from gui.main_window import MainWindow
from database.db_manager import DatabaseManager


def setup_high_dpi():
    """Configure high DPI settings for professional appearance"""
    # For PyQt6, high DPI is enabled by default
    # These attributes are handled automatically in PyQt6
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )


def main():
    """Main application entry point"""
    
    # Setup high DPI support
    setup_high_dpi()
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Museum Ticket Management System")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Museum Systems")
    
    # Set application icon (optional - uncomment if you have an icon file)
    # app.setWindowIcon(QIcon("resources/icons/app_icon.png"))
    
    # Set global font
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    # Initialize database
    db = DatabaseManager()
    
    # Create and show main window
    window = MainWindow(db)
    window.show()
    
    # Execute application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()