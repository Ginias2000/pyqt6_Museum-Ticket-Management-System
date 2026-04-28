"""
Modern Professional Stylesheet for Museum Management System
Dark Theme with Accent Colors
"""

MODERN_STYLE = """
/* Global Styles */
* {
    font-family: "Segoe UI", "Microsoft YaHei", "PingFang SC", sans-serif;
}

QMainWindow {
    background-color: #1e1e2f;
}

/* Main Window */
QMainWindow::separator {
    background-color: #2d2d3f;
    width: 1px;
    height: 1px;
}

/* Central Widget */
QWidget#centralWidget {
    background-color: #1e1e2f;
}

/* Sidebar Navigation */
QListWidget#navigation {
    background-color: #181826;
    border: none;
    border-radius: 12px;
    padding: 10px;
    margin: 10px;
    outline: none;
}

QListWidget#navigation::item {
    background-color: transparent;
    color: #a0a0c0;
    padding: 12px 16px;
    border-radius: 8px;
    margin: 2px 0;
    font-size: 14px;
}

QListWidget#navigation::item:hover {
    background-color: #2a2a3a;
    color: #ffffff;
}

QListWidget#navigation::item:selected {
    background-color: #4a6cf7;
    color: #ffffff;
}

/* Top Bar */
QWidget#topBar {
    background-color: #181826;
    border-bottom: 1px solid #2d2d3f;
}

QLabel#titleLabel {
    color: #ffffff;
    font-size: 20px;
    font-weight: bold;
}

QLabel#timeLabel {
    color: #a0a0c0;
    font-size: 14px;
}

/* Cards */
QFrame.card {
    background-color: #252535;
    border-radius: 16px;
    border: 1px solid #2d2d3f;
}

QFrame.card:hover {
    border-color: #4a6cf7;
}

/* Statistics Cards */
QFrame.stat-card {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #2d2d4a, stop:1 #252535);
    border-radius: 20px;
    border: none;
}

QLabel.stat-value {
    color: #ffffff;
    font-size: 32px;
    font-weight: bold;
}

QLabel.stat-label {
    color: #a0a0c0;
    font-size: 13px;
}

QLabel.stat-icon {
    font-size: 32px;
}

/* Buttons */
QPushButton {
    background-color: #4a6cf7;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #5d7ef8;
}

QPushButton:pressed {
    background-color: #3a5ce5;
}

QPushButton:disabled {
    background-color: #3a3a4a;
    color: #6a6a80;
}

/* Secondary Buttons */
QPushButton.btn-secondary {
    background-color: #2a2a3a;
    color: #ffffff;
}

QPushButton.btn-secondary:hover {
    background-color: #353548;
}

/* Danger Buttons */
QPushButton.btn-danger {
    background-color: #e74c3c;
}

QPushButton.btn-danger:hover {
    background-color: #c0392b;
}

/* Success Buttons */
QPushButton.btn-success {
    background-color: #27ae60;
}

QPushButton.btn-success:hover {
    background-color: #2ecc71;
}

/* Table View */
QTableView {
    background-color: #1e1e2f;
    border: none;
    border-radius: 12px;
    gridline-color: #2d2d3f;
}

QTableView::item {
    padding: 8px;
    border-bottom: 1px solid #2d2d3f;
}

QTableView::item:selected {
    background-color: #4a6cf7;
}

QHeaderView::section {
    background-color: #181826;
    color: #a0a0c0;
    padding: 10px;
    border: none;
    border-bottom: 1px solid #2d2d3f;
    font-weight: bold;
}

/* Line Edit / Input Fields */
QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    background-color: #1e1e2f;
    border: 1px solid #2d2d3f;
    border-radius: 8px;
    padding: 8px 12px;
    color: #ffffff;
    font-size: 13px;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border-color: #4a6cf7;
}

/* Scroll Bars */
QScrollBar:vertical {
    background-color: #1e1e2f;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #4a6cf7;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #5d7ef8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Tabs */
QTabWidget::pane {
    background-color: #1e1e2f;
    border: none;
    border-radius: 12px;
}

QTabBar::tab {
    background-color: #181826;
    color: #a0a0c0;
    padding: 10px 20px;
    margin-right: 4px;
    border-radius: 8px;
}

QTabBar::tab:selected {
    background-color: #4a6cf7;
    color: #ffffff;
}

QTabBar::tab:hover:!selected {
    background-color: #2a2a3a;
}

/* Progress Bar */
QProgressBar {
    background-color: #2a2a3a;
    border-radius: 4px;
    height: 6px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #27ae60;
    border-radius: 4px;
}

/* Status Bar */
QStatusBar {
    background-color: #181826;
    color: #a0a0c0;
    border-top: 1px solid #2d2d3f;
}

/* Message Box */
QMessageBox {
    background-color: #1e1e2f;
}

QMessageBox QLabel {
    color: #ffffff;
}

/* Dialog */
QDialog {
    background-color: #1e1e2f;
}

/* Tool Tips */
QToolTip {
    background-color: #2a2a3a;
    color: #ffffff;
    border: 1px solid #4a6cf7;
    border-radius: 6px;
    padding: 6px;
}

/* ComboBox Dropdown */
QComboBox QAbstractItemView {
    background-color: #1e1e2f;
    border: 1px solid #2d2d3f;
    border-radius: 8px;
    selection-background-color: #4a6cf7;
    color: #ffffff;
}

/* Calendar Widget */
QCalendarWidget {
    background-color: #1e1e2f;
}

QCalendarWidget QWidget {
    background-color: #1e1e2f;
}

/* Group Box */
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

/* Checkbox & Radio */
QCheckBox, QRadioButton {
    color: #ffffff;
    spacing: 8px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #2d2d3f;
    background-color: #1e1e2f;
}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #4a6cf7;
    border-color: #4a6cf7;
}

/* Loading Animation */
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
"""