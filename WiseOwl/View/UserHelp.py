# View/UserHelp.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class UserHelpView(QMainWindow):
    def __init__(self, user_name, member_id, role):
        super().__init__()
        self.user_name = user_name
        self.member_id = member_id
        self.role = role

        self.controller = None
        self.mybooks_callback = None
        self.history_callback = None
        self.catalog_callback = None
        self.help_callback = None
        self.logout_callback = None

        self.setWindowTitle("Wise Owl -- Help & Manual")
        try:
            self.setWindowIcon(QIcon('View/LOGO3.png'))
        except:
            pass

        self.setMinimumSize(1000, 700)
        self.resize(1400, 800)
        self.setup_ui()
        self.center()
        # Load help content after UI is set up
        self.load_help_content()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet('''
            QScrollArea {
                border: none;
                background-color: #F5F5F5;
            }
        ''')

        content = self.create_main_content()
        scroll_area.setWidget(content)

        main_layout.addWidget(scroll_area, stretch=3)

    def center(self):
        # Get a rectangle representing the window's geometry (including frame)
        qr = self.frameGeometry()
        # Get the center point of the screen's available geometry (area not covered by taskbars, etc.)
        cp = self.screen().availableGeometry().center()
        # Move the center of the window's rectangle to the screen's center point
        qr.moveCenter(cp)
        # Move the top-left point of the application window to the top-left point of the qr rectangle
        self.move(qr.topLeft())


    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet('background-color: #1C0C4F;')

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)

        # Logo section
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.setSpacing(10)

        logo_label = QLabel()
        try:
            pixmap = QPixmap('View/LOGO3.png')
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
            else:
                logo_label.setText("🦉")
                logo_label.setFont(QFont('Arial', 50))
        except:
            logo_label.setText("🦉")
            logo_label.setFont(QFont('Arial', 50))

        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)

        title_label = QLabel("WISE OWL")
        title_label.setFont(QFont('Karma', 22, QFont.Weight.Bold))
        title_label.setStyleSheet('color: white;')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(title_label)

        subtitle_label = QLabel("Library System")
        subtitle_label.setFont(QFont('Inter', 11))
        subtitle_label.setStyleSheet('color: #CCCCFF;')
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(subtitle_label)

        layout.addWidget(logo_container)
        layout.addSpacing(30)

        # User info
        user_info_label = QLabel(f"Welcome!!")
        user_info_label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        user_info_label.setStyleSheet(
            'color: white; padding: 10px;')
        user_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_info_label.setWordWrap(True)
        layout.addWidget(user_info_label)

        layout.addSpacing(20)

        # Navigation buttons - REMOVED Dashboard button
        nav_buttons = [
            ("📚 My Books", self.on_mybooks_clicked),
            ("📋 History", self.on_history_clicked),
            ("🔍 Catalog", self.on_catalog_clicked),
            ("❓ Help", self.on_help_clicked),
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
                    background-color: transparent;
                }
                QPushButton:hover {
                    background-color: #2A1A6F;
                    color: white;
                }
            ''')
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        layout.addStretch()

        logout_btn = QPushButton("🚪 Log out")
        logout_btn.clicked.connect(self.on_logout_clicked)
        logout_btn.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        logout_btn.setFixedHeight(50)
        logout_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                padding: 12px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
        ''')
        layout.addWidget(logout_btn)

        return sidebar

    def create_main_content(self):
        widget = QWidget()
        widget.setStyleSheet('background-color: #F5F5F5;')
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # Header
        header = QLabel("Help & User Manual")
        header.setFont(QFont('Karma', 36, QFont.Weight.Bold))
        header.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(header)

        subtitle = QLabel("Learn how to use the library system")
        subtitle.setFont(QFont('Inter', 16))
        subtitle.setStyleSheet('color: #596975; margin-bottom: 30px;')
        layout.addWidget(subtitle)

        # Help sections container
        self.help_container = QWidget()
        self.help_layout = QVBoxLayout(self.help_container)
        self.help_layout.setSpacing(25)
        layout.addWidget(self.help_container)

        layout.addStretch()

        return widget

    def create_help_section(self, title, items):
        """Create a help section UI"""
        widget = QWidget()
        widget.setStyleSheet('''
            QWidget {
                background-color: white;
                border-radius: 15px;
                padding: 30px;
                border: none;
            }
        ''')

        layout = QVBoxLayout(widget)
        layout.setSpacing(5)  # Reduced spacing between elements

        # Section title with icon
        title_widget = QWidget()
        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)

        # Add bullet point for section title
        bullet = QLabel("•")
        bullet.setFont(QFont('Arial', 24))
        bullet.setStyleSheet('color: #336DED;')
        title_layout.addWidget(bullet)


        title_label = QLabel(title)
        title_label.setFont(QFont('Inter', 20, QFont.Weight.Bold))
        title_label.setStyleSheet('color: #1C0C4F;')
        title_layout.addWidget(title_label)

        title_layout.addStretch()
        layout.addWidget(title_widget)

        layout.addSpacing(5)  # Small space after title

        # Create a single widget for all bullet points
        bullets_widget = QWidget()
        bullets_layout = QVBoxLayout(bullets_widget)
        bullets_layout.setContentsMargins(25, 0, 0, 0)  # Indent bullets
        bullets_layout.setSpacing(2)  # Very small spacing between bullets

        # Section items
        for item in items:
            if item.strip():
                # Each bullet point as a single label with the bullet built in
                bullet_text = f"•  {item.strip()}"  # Bullet + text
                item_label = QLabel(bullet_text)
                item_label.setFont(QFont('Inter', 12))
                item_label.setStyleSheet('color: #596975;')
                item_label.setWordWrap(True)
                bullets_layout.addWidget(item_label)
            else:
                bullets_layout.addSpacing(3)  # Small space for empty lines

        layout.addWidget(bullets_widget)
        layout.addStretch()

        return widget
    def load_help_content(self):
        """Define and load the help content"""
        help_sections = [
            {
                "title": "Getting Started",
                "items": [
                    "1. Log in to your account using your member ID",
                    "2. Navigate through the sidebar menu",
                    "3. Browse books from the catalog",
                    "4. Borrow books and manage your loans",
                    "",
                    "🟢 Your dashboard shows current loans and due dates"
                ]
            },
            {
                "title": "Managing Your Books",
                "items": [
                    "1. View current loans in 'My Books' section",
                    "2. Check due dates to avoid late fees",
                    "3. Renew books if no one is waiting",
                    "4. Return books on time",
                    "",
                    "🔴 Overdue books will incur fines"
                ]
            },
            {
                "title": "Browsing Books",
                "items": [
                    "1. Use the Catalog to search for books",
                    "2. Filter by title, author, or genre",
                    "3. Check availability status",
                    "4. Place holds on checked-out books",
                    "",
                    "🟡 Available books can be borrowed immediately"
                ]
            },
            {
                "title": "Frequently Asked Questions",
                "items": [
                    "Q: How long can I borrow books?",
                    "A: Books can be borrowed for 14 days with one renewal option.",
                    "",
                    "Q: What happens if I return a book late?",
                    "A: Late fees are $0.50 per day per book.",
                    "",
                    "Q: How do I renew my books?",
                    "A: Go to 'My Books' and click the renew button next to the book."
                ]
            }
        ]

        self.update_help_content(help_sections)

    # Callback methods
    def on_mybooks_clicked(self):
        if self.mybooks_callback:
            self.mybooks_callback()

    def on_history_clicked(self):
        if self.history_callback:
            self.history_callback()

    def on_catalog_clicked(self):
        if self.catalog_callback:
            self.catalog_callback()

    def on_help_clicked(self):
        if self.help_callback:
            self.help_callback()

    def on_logout_clicked(self):
        if self.logout_callback:
            self.logout_callback()

    def update_help_content(self, help_sections):
        """Update help content from controller"""
        while self.help_layout.count():
            item = self.help_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for section in help_sections:
            help_section = self.create_help_section(
                section["title"],
                section["items"]
            )
            self.help_layout.addWidget(help_section)

    def show_message(self, title, message, message_type="info"):
        """Show a message dialog"""
        if message_type == "info":
            QMessageBox.information(self, title, message)
        elif message_type == "warning":
            QMessageBox.warning(self, title, message)
        elif message_type == "error":
            QMessageBox.critical(self, title, message)

    def show_confirmation(self, title, message):
        """Show confirmation dialog"""
        reply = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes