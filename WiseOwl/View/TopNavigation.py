# View/TopNavigation.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class TopNavigationView(QWidget):
    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name

        self.dashboard_callback = None
        self.inventory_callback = None
        self.circulation_callback = None
        self.members_callback = None
        self.reports_callback = None
        self.settings_callback = None

        self.setFixedHeight(80)
        self.setup_ui()

    def setup_ui(self):
        """Pure UI setup with logo"""
        self.setStyleSheet('background-color: white;')  # Removed border-bottom

        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 0, 30, 0)

        # Logo/Title section with image
        logo_widget = QWidget()
        logo_layout = QHBoxLayout(logo_widget)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(15)

        # Logo image
        logo_label = QLabel()
        try:
            pixmap = QPixmap('View/LOGO3.png')
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
            else:
                logo_label.setText("🦉")
                logo_label.setFont(QFont('Arial', 32))
        except:
            logo_label.setText("🦉")
            logo_label.setFont(QFont('Arial', 32))

        logo_layout.addWidget(logo_label)

        title_label = QLabel("Wise Owl")
        title_label.setFont(QFont('Karma', 22, QFont.Weight.Bold))
        title_label.setStyleSheet('color: #1C0C4F;')
        logo_layout.addWidget(title_label)

        layout.addWidget(logo_widget)
        layout.addStretch()

        # Navigation buttons
        nav_buttons = [
            ("📊 Inventory", self.on_inventory_clicked),
            ("📄 Circulation", self.on_circulation_clicked),
            ("👥 Members", self.on_members_clicked),
            ("📈 Reports", self.on_reports_clicked),
        ]

        for text, callback in nav_buttons:
            btn = QPushButton(text)
            btn.setFont(QFont('Inter', 13))
            btn.setFixedHeight(45)
            btn.setStyleSheet('''
                QPushButton {
                    background-color: transparent;
                    color: #1C0C4F;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #F0F5FF;
                }
            ''')
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        layout.addStretch()

        # User info
        user_widget = QWidget()
        user_layout = QHBoxLayout(user_widget)
        user_layout.setContentsMargins(0, 0, 0, 0)
        user_layout.setSpacing(10)

        user_icon = QLabel("👤")
        user_icon.setFont(QFont('Arial', 20))
        user_layout.addWidget(user_icon)

        user_label = QLabel(self.user_name)
        user_label.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        user_label.setStyleSheet('color: #1C0C4F;')
        user_layout.addWidget(user_label)

        layout.addWidget(user_widget)

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