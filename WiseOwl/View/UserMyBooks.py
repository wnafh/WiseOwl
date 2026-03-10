# View/UserMyBooks.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class UserMyBooksView(QMainWindow):
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

        self.setWindowTitle("Wise Owl -- My Books")
        try:
            self.setWindowIcon(QIcon('View/LOGO3.png'))
        except:
            pass

        # Make window resizable
        self.setMinimumSize(1000, 700)
        self.resize(1300, 850)

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
        """Create sidebar UI with logo - Updated syntax"""
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
        user_info_label = QLabel(f"Welcome!!!")
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
        logout_btn.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        logout_btn.setFixedHeight(50)
        logout_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
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
        """Create main content UI - Books on LEFT, Stats on RIGHT"""
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_scroll.setStyleSheet('''
            QScrollArea {
                border: none;
                background-color: #F5F5F5;
            }
        ''')

        content_widget = QWidget()
        main_scroll.setWidget(content_widget)

        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Header section
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setSpacing(10)

        welcome_header = QLabel("My Borrowed Books")
        welcome_header.setFont(QFont('Karma', 32, QFont.Weight.Bold))
        welcome_header.setStyleSheet('color: #1C0C4F;')
        header_layout.addWidget(welcome_header)

        subtitle = QLabel("Track and manage your borrowed books")
        subtitle.setFont(QFont('Inter', 16))
        subtitle.setStyleSheet('color: #596975;')
        header_layout.addWidget(subtitle)

        layout.addWidget(header_container)

        # Two-column layout for content
        columns_widget = QWidget()
        columns_layout = QHBoxLayout(columns_widget)
        columns_layout.setSpacing(30)
        columns_layout.setContentsMargins(0, 0, 0, 0)

        # ========== LEFT COLUMN: Books List ==========
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setSpacing(20)
        left_layout.setContentsMargins(0, 0, 0, 0)

        books_header = QLabel("Currently Borrowed")
        books_header.setFont(QFont('Inter', 24, QFont.Weight.Bold))
        books_header.setStyleSheet('color: #336DED;')
        left_layout.addWidget(books_header)

        # Books container with scroll
        books_scroll = QScrollArea()
        books_scroll.setWidgetResizable(True)
        books_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        books_scroll.setStyleSheet('''
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        ''')

        self.books_container = QWidget()
        self.books_layout = QVBoxLayout(self.books_container)
        self.books_layout.setSpacing(15)
        self.books_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.books_layout.setContentsMargins(5, 5, 5, 5)

        books_scroll.setWidget(self.books_container)
        left_layout.addWidget(books_scroll)

        columns_layout.addWidget(left_column, stretch=2)  # Books take more space

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
        columns_layout.addWidget(right_column, stretch=1)  # Stats take less space

        layout.addWidget(columns_widget)
        layout.addStretch()

        return main_scroll

    def create_stat_card(self, number, label, color, icon):
        """Create a statistic card UI - Updated syntax"""
        widget = QWidget()
        widget.setMinimumHeight(110)
        widget.setStyleSheet(f'''
            QWidget {{
                background-color: white;
                border-radius: 12px;
                border: none;
            }}
        ''')

        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 15, 20, 15)

        # Icon and number row
        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(10)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont('Arial', 24))
        icon_label.setStyleSheet(f'color: {color};')
        top_layout.addWidget(icon_label)

        number_label = QLabel(str(number))
        number_label.setFont(QFont('Inter', 36, QFont.Weight.Bold))
        number_label.setStyleSheet(f'color: {color};')
        top_layout.addWidget(number_label, stretch=1)

        top_layout.addStretch()
        layout.addWidget(top_row)

        label_label = QLabel(label)
        label_label.setFont(QFont('Inter', 14))
        label_label.setStyleSheet('color: #596975;')
        label_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label_label.setWordWrap(True)
        layout.addWidget(label_label)

        return widget

    def create_book_card(self, title, author, due_date, status, days_overdue=0):
        """Create a book card UI with overdue highlighting - ABSOLUTELY NO LINES"""
        card = QWidget()
        card.setMinimumHeight(140)

        # Different background for overdue books - NO BORDERS
        if status == "Overdue":
            card.setStyleSheet('''
                QWidget {
                    background-color: #FFEBEE;
                    border-radius: 12px;
                    border: none;
                }
            ''')
        else:
            card.setStyleSheet('''
                QWidget {
                    background-color: white;
                    border-radius: 12px;
                    border: none;
                }
            ''')

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title row
        title_row = QWidget()
        title_row.setStyleSheet("background-color: transparent; border: none;")
        title_layout = QHBoxLayout(title_row)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setFont(QFont('Inter', 16, QFont.Weight.Bold))
        title_label.setStyleSheet('color: #1C0C4F; background-color: transparent; border: none;')
        title_label.setWordWrap(True)
        title_layout.addWidget(title_label, stretch=1)

        # Status badge - just colored text, no border/background
        status_badge = QLabel(status)
        status_badge.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        status_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if status == "Overdue":
            status_badge.setStyleSheet('color: #D32F2F; background-color: transparent; border: none;')
        else:
            status_badge.setStyleSheet('color: #4CAF50; background-color: transparent; border: none;')

        title_layout.addWidget(status_badge)
        layout.addWidget(title_row)

        # Author
        author_label = QLabel(f"by {author}")
        author_label.setFont(QFont('Inter', 13))
        author_label.setStyleSheet('color: #596975; background-color: transparent; border: none;')
        layout.addWidget(author_label)

        # Due date row
        due_row = QWidget()
        due_row.setStyleSheet("background-color: transparent; border: none;")
        due_layout = QHBoxLayout(due_row)
        due_layout.setContentsMargins(0, 5, 0, 5)
        due_layout.setSpacing(8)

        due_icon = QLabel("📅")
        due_icon.setFont(QFont('Arial', 14))
        due_icon.setStyleSheet("background-color: transparent; border: none;")
        due_layout.addWidget(due_icon)

        due_label = QLabel(f"Due: {due_date}")
        due_label.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        due_label.setStyleSheet("background-color: transparent; border: none;")

        if status == "Overdue":
            due_label.setStyleSheet('color: #D32F2F; background-color: transparent; border: none;')
            due_layout.addWidget(due_label)

            # Show days overdue
            if days_overdue > 0:
                days_label = QLabel(f"({days_overdue} days overdue)")
                days_label.setFont(QFont('Inter', 12))
                days_label.setStyleSheet('color: #D32F2F; background-color: transparent; border: none;')
                due_layout.addWidget(days_label)
        else:
            due_label.setStyleSheet('color: #FF9800; background-color: transparent; border: none;')
            due_layout.addWidget(due_label)

        due_layout.addStretch()
        layout.addWidget(due_row)

        # Warning message - just text
        if status == "Overdue":
            warning_label = QLabel("⚠️ Late fee will be charged")
            warning_label.setFont(QFont('Inter', 11))
            warning_label.setStyleSheet('''
                color: #D32F2F;
                background-color: transparent;
                border: none;
                margin-top: 5px;
            ''')
            layout.addWidget(warning_label)

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
    def update_books(self, books_data):
        """Update the books display with overdue highlighting"""
        # Clear existing books
        while self.books_layout.count():
            item = self.books_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Clear existing stats
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if books_data:
            # Calculate statistics with accurate overdue count
            total_books = len(books_data)
            borrowed_books = len([b for b in books_data if b.get("status") == "Borrowed"])
            overdue_books = len([b for b in books_data if b.get("status") == "Overdue"])

            # Show overdue count prominently
            print(f"📊 UI Update - Overdue books: {overdue_books}")

            # Update stats cards with overdue count highlighted
            stats = [
                {"number": str(total_books), "label": "Total Books", "color": "#336DED", "icon": "📚"},
                {"number": str(borrowed_books), "label": "Currently Reading", "color": "#4CAF50", "icon": "📖"},
                {"number": str(overdue_books), "label": "Overdue", "color": "#F44336", "icon": "⚠️"},
            ]

            for stat in stats:
                stat_card = self.create_stat_card(stat["number"], stat["label"], stat["color"], stat["icon"])
                self.stats_layout.addWidget(stat_card)

            # Add books with overdue first
            # Sort books: Overdue first, then by due date
            sorted_books = sorted(books_data,
                                  key=lambda x: (0 if x.get("status") == "Overdue" else 1,
                                                 x.get("due_date", "")))

            for book in sorted_books:
                title = book.get("title", "Unknown Title")
                author = book.get("author", "Unknown Author")
                due_date = book.get("due_date", "No due date")
                status = book.get("status", "Unknown")
                days_overdue = book.get("days_overdue", 0)

                book_card = self.create_book_card(title, author, due_date, status, days_overdue)
                self.books_layout.addWidget(book_card)

                # Add separator after overdue books if there are both overdue and regular
                if status == "Overdue" and any(b.get("status") != "Overdue" for b in books_data):
                    separator = QFrame()
                    separator.setFrameShape(QFrame.Shape.HLine)
                    separator.setStyleSheet("background-color: #FFCDD2; max-height: 2px; margin: 10px 0;")
                    self.books_layout.addWidget(separator)
        else:
            # Show default stats
            default_stats = [
                {"number": "0", "label": "Total Books", "color": "#336DED", "icon": "📚"},
                {"number": "0", "label": "Currently Reading", "color": "#4CAF50", "icon": "📖"},
                {"number": "0", "label": "Overdue", "color": "#F44336", "icon": "⚠️"},
            ]

            for stat in default_stats:
                stat_card = self.create_stat_card(stat["number"], stat["label"], stat["color"], stat["icon"])
                self.stats_layout.addWidget(stat_card)

            # Show placeholder if no books
            no_books = QLabel("You haven't borrowed any books yet.")
            no_books.setFont(QFont('Inter', 14))
            no_books.setStyleSheet('color: #9E9E9E; padding: 40px;')
            no_books.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.books_layout.addWidget(no_books)

        self.books_layout.addStretch()

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

    def set_controller(self, controller):
        """Set the controller reference"""
        self.controller = controller