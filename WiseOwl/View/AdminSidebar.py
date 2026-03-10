# View/AdminSidebar.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class AdminSidebarView(QWidget):
    def __init__(self, user_name, member_id, role):
        super().__init__()
        self.user_name = user_name
        self.member_id = member_id
        self.role = role

        self.dashboard_callback = None
        self.inventory_callback = None
        self.circulation_callback = None
        self.members_callback = None
        self.reports_callback = None
        self.settings_callback = None
        self.logout_callback = None

        self.setFixedWidth(280)
        self.setStyleSheet('background-color: #1C0C4F;')
        self.setup_ui()



    def setup_ui(self):
        """Pure UI setup with logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 25, 20, 25)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)

        # Logo section
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.setSpacing(10)

        # Try to load actual logo
        logo_label = QLabel()
        try:
            pixmap = QPixmap('View/LOGO3.png')
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
            else:
                logo_label.setText("🦉")
                logo_label.setFont(QFont('Arial', 40))
                logo_label.setStyleSheet('color: white;')
        except:
            logo_label.setText("🦉")
            logo_label.setFont(QFont('Arial', 40))
            logo_label.setStyleSheet('color: white;')

        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)

        # Title
        title_label = QLabel("WISE OWL")
        title_label.setFont(QFont('Karma', 20, QFont.Weight.Bold))
        title_label.setStyleSheet('color: white;')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(title_label)

        subtitle_label = QLabel("Admin Panel")
        subtitle_label.setFont(QFont('Inter', 11))
        subtitle_label.setStyleSheet('color: #CCCCFF;')
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(subtitle_label)

        layout.addWidget(logo_container)
        layout.addSpacing(20)

        # Navigation buttons
        nav_buttons = [
            ("📊 Dashboard", self.on_dashboard_clicked),
            ("📚 Inventory", self.on_inventory_clicked),
            ("📄 Circulation", self.on_circulation_clicked),
            ("👥 Members", self.on_members_clicked),
            ("📈 Reports", self.on_reports_clicked),
        ]

        for text, callback in nav_buttons:
            btn = QPushButton(text)
            btn.setFont(QFont('Inter', 13))
            btn.setFixedHeight(50)
            btn.setStyleSheet('''
                QPushButton {
                    text-align: left;
                    padding-left: 20px;
                    border: none;
                    border-radius: 8px;
                    color: #CCCCFF;
                    background-color: #1C0C4F;
                }
                QPushButton:hover {
                    background-color: #2A1A6F;
                    color: white;
                }
            ''')
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        layout.addStretch()

        # Stats section at bottom
        stats_widget = QWidget()
        stats_widget.setStyleSheet('''
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
        ''')
        stats_layout = QVBoxLayout(stats_widget)
        stats_layout.setSpacing(10)

        stats_title = QLabel("Library Stats")
        stats_title.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        stats_title.setStyleSheet('color: white;')
        stats_layout.addWidget(stats_title)

        # Stats items
        stats_items = [
            ("Total Books", "1,234"),
            ("Available", "987"),
            ("Borrowed", "234"),
            ("Missing", "13"),
        ]

        for label, value in stats_items:
            stat_widget = QWidget()
            stat_layout = QHBoxLayout(stat_widget)
            stat_layout.setContentsMargins(0, 0, 0, 0)

            label_widget = QLabel(label)
            label_widget.setFont(QFont('Inter', 11))
            label_widget.setStyleSheet('color: #CCCCFF;')
            stat_layout.addWidget(label_widget)

            stat_layout.addStretch()

            value_widget = QLabel(value)
            value_widget.setFont(QFont('Inter', 11, QFont.Weight.Bold))
            value_widget.setStyleSheet('color: white;')
            stat_layout.addWidget(value_widget)

            stats_layout.addWidget(stat_widget)

        layout.addWidget(stats_widget)
        layout.addSpacing(15)

        # Logout button
        logout_btn = QPushButton("🚪 Log out")
        logout_btn.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        logout_btn.setFixedHeight(50)
        logout_btn.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                color: #CCCCFF;
                padding: 10px;
                border-radius: 8px;
                border: 2px solid #CCCCFF;
            }
            QPushButton:hover {
                background-color: #2958C4;
                color: white;
                border-color: #2958C4;
            }
        ''')
        logout_btn.clicked.connect(self.on_logout_clicked)
        layout.addWidget(logout_btn)

    # Callback methods
    def on_dashboard_clicked(self):
        if self.dashboard_callback:
            self.dashboard_callback()

    def on_inventory_clicked(self):
        if self.inventory_callback:
            self.inventory_callback()

    def on_circulation_clicked(self):
        if self.circulation_callback:
            self.circulation_callback()

    def on_members_clicked(self):
        if self.members_callback:
            self.members_callback()

    def on_reports_clicked(self):
        if self.reports_callback:
            self.reports_callback()

    def on_settings_clicked(self):
        if self.settings_callback:
            self.settings_callback()

    def on_logout_clicked(self):
        if self.logout_callback:
            self.logout_callback()