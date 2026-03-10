# View/UserCatalog.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class UserCatalogView(QMainWindow):
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
        self.search_callback = None
        self.filter_callback = None
        self.view_details_callback = None

        self.current_filter = "All Books"

        self.setWindowTitle("Wise Owl -- Library Catalog")
        try:
            self.setWindowIcon(QIcon('View/LOGO3.png'))
        except:
            pass

        # Make window resizable
        self.setMinimumSize(1000, 700)
        self.resize(1400, 900)

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
                    border-radius: 10px;
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
                border-radius: 10px;
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
        """Create main content UI"""
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_scroll.setStyleSheet('QScrollArea { border: none; background-color: #F5F5F5; }')

        content_widget = QWidget()
        main_scroll.setWidget(content_widget)

        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Header
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setSpacing(10)

        welcome_header = QLabel("Library Catalog")
        welcome_header.setFont(QFont('Karma', 32, QFont.Weight.Bold))
        welcome_header.setStyleSheet('color: #1C0C4F;')
        header_layout.addWidget(welcome_header)

        subtitle = QLabel("Browse and search for books in the library")
        subtitle.setFont(QFont('Inter', 16))
        subtitle.setStyleSheet('color: #596975;')
        header_layout.addWidget(subtitle)

        layout.addWidget(header_container)

        # Search and filter bar
        search_filter_widget = QWidget()
        search_filter_layout = QHBoxLayout(search_filter_widget)
        search_filter_layout.setContentsMargins(0, 0, 0, 0)
        search_filter_layout.setSpacing(15)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title, author, or genre...")
        self.search_input.setFont(QFont('Inter', 14))
        self.search_input.setFixedHeight(50)
        self.search_input.setStyleSheet('''
            QLineEdit {
                padding: 0 20px;
                border: none;
                border-radius: 10px;
                background-color: white;
            }
            QLineEdit:focus {
                border: none;
            }
        ''')
        self.search_input.returnPressed.connect(self.on_search_clicked)
        search_filter_layout.addWidget(self.search_input, stretch=3)

        # Filter dropdown
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(
            ["All Books", "Available Only", "Fiction", "Non-Fiction", "Fantasy", "Romance", "Mystery"])
        self.filter_combo.setFont(QFont('Inter', 14))
        self.filter_combo.setFixedHeight(50)
        self.filter_combo.setStyleSheet('''
            QComboBox {
                padding: 0 20px;
                border: none;
                border-radius: 10px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
        ''')
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        search_filter_layout.addWidget(self.filter_combo, stretch=1)

        # Search button
        search_btn = QPushButton("🔍 Search")
        search_btn.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        search_btn.setFixedHeight(50)
        search_btn.setFixedWidth(120)
        search_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
        ''')
        search_btn.clicked.connect(self.on_search_clicked)
        search_filter_layout.addWidget(search_btn)

        layout.addWidget(search_filter_widget)

        # Results info
        self.results_label = QLabel("")
        self.results_label.setFont(QFont('Inter', 14))
        self.results_label.setStyleSheet('color: #596975;')
        layout.addWidget(self.results_label)

        # Books grid container
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet('QScrollArea { border: none; background-color: transparent; }')

        self.books_grid_container = QWidget()
        self.books_grid_layout = QVBoxLayout(self.books_grid_container)
        self.books_grid_layout.setSpacing(20)
        self.books_grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll_area.setWidget(self.books_grid_container)
        layout.addWidget(scroll_area)

        return main_scroll

    def create_book_card(self, book_id, title, author, status, genre, description, available_copies):
        """Create a clean book card UI without borders"""
        card = QWidget()
        card.setMinimumHeight(180)
        card.setStyleSheet('''
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
        ''')

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 30))
        card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(12)

        # Title and status row
        title_row = QWidget()
        title_layout = QHBoxLayout(title_row)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(15)

        title_label = QLabel(title)
        title_label.setFont(QFont('Inter', 20, QFont.Weight.Bold))
        title_label.setStyleSheet('color: #1C0C4F;')
        title_label.setWordWrap(True)
        title_layout.addWidget(title_label, stretch=1)

        # Status badge (simplified without borders)
        status_label = QLabel(status)
        status_label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        status_label.setFixedHeight(32)
        status_label.setFixedWidth(100)
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if status == "Available":
            status_label.setStyleSheet('''
                color: #4CAF50;
                background-color: transparent;
                padding: 6px;
                border-radius: 0;
            ''')
        else:
            status_label.setStyleSheet('''
                color: #9E9E9E;
                background-color: transparent;
                padding: 6px;
                border-radius: 0;
            ''')
        title_layout.addWidget(status_label)

        layout.addWidget(title_row)

        # Author
        author_label = QLabel(f"by {author}")
        author_label.setFont(QFont('Inter', 15))
        author_label.setStyleSheet('color: #596975;')
        layout.addWidget(author_label)

        # Info row (Genre and Available copies)
        info_row = QWidget()
        info_layout = QHBoxLayout(info_row)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(20)

        # Genre
        genre_label = QLabel(f"📖 {genre}")
        genre_label.setFont(QFont('Inter', 13))
        genre_label.setStyleSheet('color: #757575;')
        info_layout.addWidget(genre_label)

        # Available copies
        copies_label = QLabel(f"📚 {available_copies} available")
        copies_label.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        copies_label.setStyleSheet('color: #336DED;')
        info_layout.addWidget(copies_label)

        info_layout.addStretch()
        layout.addWidget(info_row)

        # Description (truncated)
        if description:
            desc_label = QLabel(description[:120] + "..." if len(description) > 120 else description)
            desc_label.setFont(QFont('Inter', 13))
            desc_label.setStyleSheet('color: #757575; margin-top: 5px;')
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        layout.addSpacing(10)

        # View Details button only
        details_btn = QPushButton("View Details")
        details_btn.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        details_btn.setFixedHeight(45)
        details_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
        ''')
        details_btn.clicked.connect(lambda: self.on_view_details_clicked(book_id))
        layout.addWidget(details_btn)

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

    def on_search_clicked(self):
        query = self.search_input.text().strip()
        if self.search_callback:
            self.search_callback(query)

    def on_filter_changed(self, filter_text):
        self.current_filter = filter_text
        if self.filter_callback:
            self.filter_callback(filter_text)

    def on_view_details_clicked(self, book_id):
        if self.view_details_callback:
            self.view_details_callback(book_id)

    # Methods for Controller to call
    def update_books(self, books_data, search_query="", filter_text=""):
        """Update the books display"""
        # Clear existing books
        while self.books_grid_layout.count():
            item = self.books_grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if books_data:
            # Update results label
            result_text = f"Found {len(books_data)} book(s)"
            if search_query:
                result_text += f" for '{search_query}'"
            if filter_text and filter_text != "All Books":
                result_text += f" (Filtered: {filter_text})"
            self.results_label.setText(result_text)

            # Add books
            for book in books_data:
                book_card = self.create_book_card(
                    book.get("book_id", ""),
                    book.get("title", "Unknown Title"),
                    book.get("author", "Unknown Author"),
                    book.get("status", "Unknown"),
                    book.get("genre", "Unknown"),
                    book.get("description", ""),
                    book.get("available_copies", 0)
                )
                self.books_grid_layout.addWidget(book_card)
        else:
            # Show empty state
            if search_query:
                self.results_label.setText(f"No books found for '{search_query}'")
                empty_label = QLabel(f"No books found for '{search_query}'\n\nTry a different search term")
            else:
                self.results_label.setText("No books available")
                empty_label = QLabel("No books available in the catalog")

            empty_label.setFont(QFont('Inter', 16))
            empty_label.setStyleSheet('color: #9E9E9E; padding: 80px;')
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.books_grid_layout.addWidget(empty_label)

        self.books_grid_layout.addStretch()

    def show_book_details(self, book_details):
        """Show book details dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Book Details")
        dialog.setMinimumSize(550, 650)
        dialog.setStyleSheet('QDialog { background-color: white; }')

        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title_label = QLabel(book_details["title"])
        title_label.setFont(QFont('Inter', 26, QFont.Weight.Bold))
        title_label.setStyleSheet('color: #1C0C4F;')
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # Author
        author_label = QLabel(f"by {book_details['author']}")
        author_label.setFont(QFont('Inter', 18))
        author_label.setStyleSheet('color: #596975;')
        layout.addWidget(author_label)

        layout.addSpacing(10)

        # Details section (simplified without borders)
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details_layout.setSpacing(12)

        details = [
            ("📖 Genre", book_details.get("genre", "N/A")),
            ("📊 Status", book_details.get("status", "N/A")),
            ("📚 Available Copies", str(book_details.get("available_copies", 0))),
            ("📦 Total Copies", str(book_details.get("total_copies", 0))),
            ("📍 Location", book_details.get("location", "N/A")),
        ]

        for label, value in details:
            detail_row = QWidget()
            detail_layout = QHBoxLayout(detail_row)
            detail_layout.setContentsMargins(0, 0, 0, 0)

            label_widget = QLabel(label)
            label_widget.setFont(QFont('Inter', 14, QFont.Weight.Bold))
            label_widget.setStyleSheet('color: #1C0C4F;')
            detail_layout.addWidget(label_widget)

            detail_layout.addStretch()

            value_widget = QLabel(str(value))
            value_widget.setFont(QFont('Inter', 14))
            value_widget.setStyleSheet('color: #596975;')
            detail_layout.addWidget(value_widget)

            details_layout.addWidget(detail_row)

        layout.addWidget(details_widget)

        # Description
        layout.addSpacing(5)
        desc_label = QLabel("Description")
        desc_label.setFont(QFont('Inter', 15, QFont.Weight.Bold))
        desc_label.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(desc_label)

        desc_text = QTextEdit()
        desc_text.setText(book_details.get("description", "No description available."))
        desc_text.setReadOnly(True)
        desc_text.setMaximumHeight(150)
        desc_text.setStyleSheet('''
            QTextEdit {
                border: none;
                border-radius: 0;
                padding: 0;
                background-color: transparent;
                font-size: 13px;
                color: #596975;
            }
        ''')
        layout.addWidget(desc_text)

        layout.addStretch()

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        close_btn.setFixedHeight(50)
        close_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
        ''')
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec()

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