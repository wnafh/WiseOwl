## View/UserHistory.py -
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class UserHistoryView(QMainWindow):
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

        self.setWindowTitle("Wise Owl -- Borrowing History")
        try:
            self.setWindowIcon(QIcon('View/LOGO3.png'))
        except:
            pass

        # Make window resizable
        self.setMinimumSize(1000, 700)
        self.resize(1400, 800)

        self.setup_ui()

        self.center()

    def setup_ui(self):
        """Pure UI setup"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        content = self.create_main_content()
        main_layout.addWidget(content, stretch=4)

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
        """Create sidebar UI with logo"""
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

        # Navigation buttons
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

        # Logout button
        logout_btn = QPushButton("🚪 Log out")
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
        logout_btn.clicked.connect(self.on_logout_clicked)
        layout.addWidget(logout_btn)

        return sidebar

    def create_main_content(self):
        """Create main content UI - EXPANDED HISTORY SECTION"""
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_scroll.setStyleSheet('QScrollArea { border: none; background-color: #F5F5F5; }')

        content_widget = QWidget()
        main_scroll.setWidget(content_widget)

        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Header section
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setSpacing(10)

        welcome_header = QLabel("Borrowing History")
        welcome_header.setFont(QFont('Karma', 32, QFont.Weight.Bold))
        welcome_header.setStyleSheet('color: #1C0C4F;')
        header_layout.addWidget(welcome_header)

        subtitle = QLabel("Your past borrowed books")
        subtitle.setFont(QFont('Inter', 16))
        subtitle.setStyleSheet('color: #596975;')
        header_layout.addWidget(subtitle)

        layout.addWidget(header_container)

        # Two-column layout with ADJUSTED RATIO - History gets more space
        columns_widget = QWidget()
        columns_layout = QHBoxLayout(columns_widget)
        columns_layout.setSpacing(30)
        columns_layout.setContentsMargins(0, 0, 0, 0)

        # ========== LEFT COLUMN: History list - EXPANDED ==========
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setSpacing(20)
        left_layout.setContentsMargins(0, 0, 0, 0)

        history_header = QLabel("All History")
        history_header.setFont(QFont('Inter', 24, QFont.Weight.Bold))
        history_header.setStyleSheet('color: #1C0C4F;')
        left_layout.addWidget(history_header)

        # History container with scroll - TAKES FULL WIDTH
        history_scroll = QScrollArea()
        history_scroll.setWidgetResizable(True)
        history_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        history_scroll.setStyleSheet('''
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #C1C1C1;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #A8A8A8;
            }
        ''')

        self.history_container = QWidget()
        self.history_layout = QVBoxLayout(self.history_container)
        self.history_layout.setSpacing(15)
        self.history_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.history_layout.setContentsMargins(0, 0, 10, 0)  # Right margin for scrollbar

        history_scroll.setWidget(self.history_container)
        left_layout.addWidget(history_scroll)

        # LEFT COLUMN GETS MORE SPACE (3:1 ratio instead of 2:1)
        columns_layout.addWidget(left_column, stretch=3)

        # ========== RIGHT COLUMN: Statistics ==========
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setSpacing(20)
        right_layout.setContentsMargins(0, 0, 0, 0)

        stats_header = QLabel("Reading Statistics")
        stats_header.setFont(QFont('Inter', 24, QFont.Weight.Bold))
        stats_header.setStyleSheet('color: #1C0C4F;')
        right_layout.addWidget(stats_header)

        # Stats cards container
        self.stats_container = QWidget()
        self.stats_layout = QVBoxLayout(self.stats_container)
        self.stats_layout.setSpacing(15)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self.stats_container)

        right_layout.addStretch()
        columns_layout.addWidget(right_column, stretch=1)

        layout.addWidget(columns_widget)
        layout.addStretch()

        return main_scroll

    def create_stat_card(self, number, label, color):
        """Create a statistic card UI"""
        widget = QWidget()
        widget.setMinimumHeight(100)
        widget.setStyleSheet(f'''
            QWidget {{
                background-color: white;
                border-radius: 12px;
                border: none;
            }}
        ''')

        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        number_label = QLabel(str(number))
        number_label.setFont(QFont('Inter', 36, QFont.Weight.Bold))
        number_label.setStyleSheet(f'color: {color};')
        number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(number_label)

        label_label = QLabel(label)
        label_label.setFont(QFont('Inter', 14))
        label_label.setStyleSheet('color: #596975;')
        label_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_label.setWordWrap(True)
        layout.addWidget(label_label)

        return widget

    def create_history_card(self, title, author, borrowed, returned, status):
        """Create a history card UI - WIDER"""
        card = QWidget()
        card.setMinimumHeight(130)
        card.setMaximumWidth(1200)  # Allow it to expand
        card.setStyleSheet('''
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: none;
            }
        ''')

        layout = QVBoxLayout(card)
        layout.setContentsMargins(30, 22, 30, 22)
        layout.setSpacing(10)

        # Title row
        title_row = QWidget()
        title_row.setStyleSheet("background-color: transparent; border: none;")
        title_layout = QHBoxLayout(title_row)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(15)

        title_label = QLabel(title)
        title_label.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        title_label.setStyleSheet('color: #1C0C4F; background-color: transparent; border: none;')
        title_label.setWordWrap(True)
        title_layout.addWidget(title_label, stretch=1)

        # Status badge
        status_badge = QLabel(status)
        status_badge.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        status_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if status == "Returned":
            status_badge.setStyleSheet('color: #4CAF50; background-color: transparent; border: none;')
        elif status == "Borrowed":
            status_badge.setStyleSheet('color: #FF9800; background-color: transparent; border: none;')
        else:
            status_badge.setStyleSheet('color: #757575; background-color: transparent; border: none;')

        title_layout.addWidget(status_badge)
        layout.addWidget(title_row)

        # Author
        author_label = QLabel(f"by {author}")
        author_label.setFont(QFont('Inter', 14))
        author_label.setStyleSheet('color: #596975; background-color: transparent; border: none;')
        layout.addWidget(author_label)

        # Dates row - SPREAD OUT FOR BETTER READABILITY
        dates_row = QWidget()
        dates_row.setStyleSheet("background-color: transparent; border: none;")
        dates_layout = QHBoxLayout(dates_row)
        dates_layout.setContentsMargins(0, 5, 0, 0)
        dates_layout.setSpacing(40)  # Increased spacing

        borrowed_label = QLabel(f"📅 Borrowed: {borrowed}")
        borrowed_label.setFont(QFont('Inter', 13))
        borrowed_label.setStyleSheet('color: #596975; background-color: transparent; border: none;')
        dates_layout.addWidget(borrowed_label)

        returned_label = QLabel(f"📅 Returned: {returned}")
        returned_label.setFont(QFont('Inter', 13))
        returned_label.setStyleSheet('color: #596975; background-color: transparent; border: none;')
        dates_layout.addWidget(returned_label)

        dates_layout.addStretch()
        layout.addWidget(dates_row)

        return card

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

    # Methods for Controller to call
    def update_history(self, history_data):
        """Update the history display - EXPANDED VIEW"""
        # Clear existing history
        while self.history_layout.count():
            item = self.history_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Clear existing stats
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if history_data:
            # Calculate statistics
            total_books = len(history_data)
            returned_on_time = len(
                [h for h in history_data if h.get("status") == "Returned"])
            late_returns = len(
                [h for h in history_data if "Overdue" in str(h.get("status", ""))])

            # Update stats
            stats = [
                {"number": str(total_books), "label": "Total Books Read", "color": "#336DED"},
                {"number": str(returned_on_time), "label": "Returned On Time", "color": "#4CAF50"},
                {"number": str(late_returns), "label": "Late Returns", "color": "#F44336"},
            ]

            for stat in stats:
                stat_card = self.create_stat_card(stat["number"], stat["label"], stat["color"])
                self.stats_layout.addWidget(stat_card)

            # Add history cards - SORTED BY DATE (most recent first)
            # Assuming history_data is already sorted, but we can sort by borrowed date
            for item in history_data:
                history_card = self.create_history_card(
                    item.get("title", "Unknown Title"),
                    item.get("author", "Unknown Author"),
                    item.get("borrowed", "Unknown"),
                    item.get("returned", "Not returned"),
                    item.get("status", "Unknown")
                )
                self.history_layout.addWidget(history_card)
        else:
            # Show default stats
            default_stats = [
                {"number": "0", "label": "Total Books Read", "color": "#336DED"},
                {"number": "0", "label": "Returned On Time", "color": "#4CAF50"},
                {"number": "0", "label": "Late Returns", "color": "#F44336"},
            ]

            for stat in default_stats:
                stat_card = self.create_stat_card(stat["number"], stat["label"], stat["color"])
                self.stats_layout.addWidget(stat_card)

            # Show placeholder - CENTERED AND BIGGER
            no_history_container = QWidget()
            no_history_layout = QVBoxLayout(no_history_container)
            no_history_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            no_history = QLabel("📚 No borrowing history yet.\n\nStart borrowing books to see your history here!")
            no_history.setFont(QFont('Inter', 16))
            no_history.setStyleSheet('color: #9E9E9E; padding: 60px;')
            no_history.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_history_layout.addWidget(no_history)

            self.history_layout.addWidget(no_history_container)

        self.history_layout.addStretch()

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