# View/AdminInventory.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class AdminInventoryView(QMainWindow):
    def __init__(self, user_name, member_id, role):
        super().__init__()
        self.user_name = user_name
        self.member_id = member_id
        self.role = role

        self.controller = None
        self.dashboard_callback = None
        self.inventory_callback = None
        self.circulation_callback = None
        self.members_callback = None
        self.reports_callback = None
        self.settings_callback = None
        self.logout_callback = None
        self.search_book_callback = None
        # Removed filter_book_callback
        self.add_book_callback = None
        self.edit_book_callback = None
        self.delete_book_callback = None

        self.setWindowTitle("Wise Owl -- Inventory Management")
        try:
            self.setWindowIcon(QIcon('View/LOGO3.png'))
        except:
            pass

        self.setMinimumSize(1280, 720)
        self.resize(1440, 900)

        self.books_data = []
        self.setup_ui()
        self.center()

    def setup_ui(self):
        """Pure UI setup with optimized spacing"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        content = self.create_main_content()
        main_layout.addWidget(content, stretch=1)

    def create_sidebar(self):
        """Create sidebar UI with logo"""
        from View.AdminSidebar import AdminSidebarView

        sidebar = AdminSidebarView(self.user_name, self.member_id, self.role)
        sidebar.dashboard_callback = self.on_dashboard_clicked
        sidebar.inventory_callback = self.on_inventory_clicked
        sidebar.circulation_callback = self.on_circulation_clicked
        sidebar.members_callback = self.on_members_clicked
        sidebar.reports_callback = self.on_reports_clicked
        sidebar.settings_callback = self.on_settings_clicked
        sidebar.logout_callback = self.on_logout_clicked

        return sidebar

    def create_main_content(self):
        """Create main content UI with optimized layout"""
        widget = QWidget()
        widget.setStyleSheet('background-color: #F5F5F5;')
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Top section
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setSpacing(12)
        top_layout.setContentsMargins(0, 0, 0, 0)

        # Header row
        header_row = QWidget()
        header_layout = QHBoxLayout(header_row)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        header = QLabel("📚 Inventory Management")
        header.setFont(QFont('Karma', 28, QFont.Weight.Bold))
        header.setStyleSheet('color: #1C0C4F;')
        header_layout.addWidget(header)

        header_layout.addStretch()

        # Add book button
        add_btn = QPushButton("➕ Add New Book")
        add_btn.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        add_btn.setFixedHeight(50)
        add_btn.setFixedWidth(170)
        add_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3D8B40;
            }
        ''')
        add_btn.clicked.connect(self.on_add_book_clicked)
        header_layout.addWidget(add_btn)

        top_layout.addWidget(header_row)

        subtitle = QLabel("View, add, edit, and manage library inventory")
        subtitle.setFont(QFont('Inter', 14))
        subtitle.setStyleSheet('color: #596975;')
        top_layout.addWidget(subtitle)

        layout.addWidget(top_widget)

        # Search bar - removed filter dropdown
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Title, Author, or Genre...")
        self.search_input.setFont(QFont('Inter', 13))
        self.search_input.setFixedHeight(45)
        self.search_input.setStyleSheet('''
            QLineEdit {
                padding: 0 16px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #336DED;
            }
        ''')
        self.search_input.returnPressed.connect(self.on_search_clicked)
        search_layout.addWidget(self.search_input, stretch=1)

        search_btn = QPushButton("🔍 Search")
        search_btn.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        search_btn.setFixedHeight(45)
        search_btn.setFixedWidth(110)
        search_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
        ''')
        search_btn.clicked.connect(self.on_search_clicked)
        search_layout.addWidget(search_btn)

        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        refresh_btn.setFixedHeight(45)
        refresh_btn.setFixedWidth(110)
        refresh_btn.setStyleSheet('''
            QPushButton {
                background-color: #607D8B;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #546E7A;
            }
        ''')
        refresh_btn.clicked.connect(self.on_refresh_clicked)
        search_layout.addWidget(refresh_btn)

        layout.addWidget(search_widget)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setFont(QFont('Inter', 12))
        self.status_label.setStyleSheet('color: #596975;')
        layout.addWidget(self.status_label)

        # Books scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet('''
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #C1C1C1;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #A8A8A8;
            }
        ''')

        self.books_container = QWidget()
        self.books_layout = QVBoxLayout(self.books_container)
        self.books_layout.setSpacing(16)
        self.books_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.books_layout.setContentsMargins(2, 2, 2, 2)

        scroll_area.setWidget(self.books_container)
        layout.addWidget(scroll_area, stretch=1)

        return widget

    #Centers the widget
    def center(self):
        # Get a rectangle representing the window's geometry (including frame)
        qr = self.frameGeometry()
        # Get the center point of the screen's available geometry (area not covered by taskbars, etc.)
        cp = self.screen().availableGeometry().center()
        # Move the center of the window's rectangle to the screen's center point
        qr.moveCenter(cp)
        # Move the top-left point of the application window to the top-left point of the qr rectangle
        self.move(qr.topLeft())
    def create_book_card(self, book_index, book_data):
        """Create book card WITHOUT border lines between text sections"""
        card = QWidget()
        card.setMinimumHeight(120)
        card.setStyleSheet('''
            QWidget {
                background-color: white;
                border: none;
                border-radius: 6px;
            }
            QWidget:hover {
                background-color: #F8F9FA;
            }
        ''')

        layout = QHBoxLayout(card)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(18)

        # Book info - clean, no visual separation
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(4)

        title = book_data.get("title", "Unknown Title")
        author = book_data.get("author", "Unknown Author")
        genre = book_data.get("genre", "No Genre")
        location = book_data.get("location", "No Location")
        total_copies = book_data.get("total_copies", 0)
        available_copies = book_data.get("available_copies", 0)

        title_label = QLabel(title)
        title_label.setFont(QFont('Inter', 15, QFont.Weight.Bold))
        title_label.setStyleSheet('color: #1C0C4F;')
        title_label.setWordWrap(True)
        info_layout.addWidget(title_label)

        author_label = QLabel(f"by {author}")
        author_label.setFont(QFont('Inter', 12))
        author_label.setStyleSheet('color: #596975;')
        info_layout.addWidget(author_label)

        details_label = QLabel(f"{genre} • {location}")
        details_label.setFont(QFont('Inter', 11))
        details_label.setStyleSheet('color: #9E9E9E;')
        info_layout.addWidget(details_label)

        layout.addWidget(info_widget)
        layout.addStretch()

        # Stats - clean, no visual separation
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        stats_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.setSpacing(2)

        total_copies_int = int(total_copies) if total_copies is not None else 0
        available_copies_int = int(available_copies) if available_copies is not None else 0

        copies_label = QLabel(f"Total: {total_copies_int}")
        copies_label.setFont(QFont('Inter', 12))
        copies_label.setStyleSheet('color: #596975;')
        stats_layout.addWidget(copies_label)

        avail_label = QLabel(f"Available: {available_copies_int}")
        avail_label.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        if available_copies_int > 0:
            avail_label.setStyleSheet('color: #4CAF50;')
        else:
            avail_label.setStyleSheet('color: #F44336;')
        stats_layout.addWidget(avail_label)

        layout.addWidget(stats_widget)

        # Status badge - clean text without box border
        status_text = "Available" if available_copies_int > 0 else "Not Available"
        status_label = QLabel(status_text)
        status_label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if available_copies_int > 0:
            status_label.setStyleSheet('color: #4CAF50;')
        else:
            status_label.setStyleSheet('color: #F44336;')
        layout.addWidget(status_label)

        # Action buttons - clean, no visual separation
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(8)

        edit_btn = QPushButton("✏️ Edit")
        edit_btn.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        edit_btn.setFixedSize(85, 35)
        edit_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
        ''')
        edit_btn.clicked.connect(lambda checked, idx=book_index: self.on_edit_book_clicked(idx))
        actions_layout.addWidget(edit_btn)

        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        delete_btn.setFixedSize(85, 35)
        delete_btn.setStyleSheet('''
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        ''')
        delete_btn.clicked.connect(lambda checked, idx=book_index: self.on_delete_book_clicked(idx))
        actions_layout.addWidget(delete_btn)

        layout.addWidget(actions_widget)

        return card

    def create_stat_card(self, number, label, color, icon):
        """Create a stat card widget"""
        widget = QWidget()
        widget.setMinimumHeight(100)
        widget.setStyleSheet('''
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
        ''')

        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(5)

        # Icon and number
        icon_label = QLabel(f"{icon} {number}")
        icon_label.setFont(QFont('Inter', 24, QFont.Weight.Bold))
        icon_label.setStyleSheet(f'color: {color};')
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        # Label
        label_label = QLabel(label)
        label_label.setFont(QFont('Inter', 12))
        label_label.setStyleSheet('color: #596975;')
        label_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_label)

        return widget

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

    def on_search_clicked(self):
        query = self.search_input.text().strip()
        if self.search_book_callback:
            self.search_book_callback(query)

    # Removed on_filter_changed method

    def on_refresh_clicked(self):
        if self.search_book_callback:
            self.search_book_callback("")
            self.search_input.clear()
            # Removed filter combo reset

    def on_add_book_clicked(self):
        """Show add book dialog"""
        from View.Dialogs import AddBookDialog

        dialog = AddBookDialog(self)

        def process_dialog():
            book_data = dialog.get_book_data()

            if not book_data["title"] or not book_data["author"]:
                self.show_message("Validation Error", "Title and Author are required!", "error")
                return

            if self.add_book_callback:
                book_data["available_copies"] = book_data["total_copies"]
                self.add_book_callback(book_data)
                dialog.accept()

        dialog.add_btn.clicked.connect(process_dialog)
        dialog.exec()

    def on_edit_book_clicked(self, book_index):
        """Show edit book dialog"""
        if book_index < len(self.books_data):
            book_data = self.books_data[book_index]

            if "book_id" not in book_data:
                self.show_message("Error", "Book ID is missing! Cannot edit this book.", "error")
                return

            from View.Dialogs import EditBookDialog

            dialog = EditBookDialog(
                book_title=book_data.get("title", ""),
                current_data=book_data,
                parent=self
            )

            def process_edit():
                updated_data = dialog.get_updated_data()

                if not updated_data["title"] or not updated_data["author"]:
                    self.show_message("Validation Error", "Title and Author are required!", "error")
                    return

                updated_data["book_id"] = book_data.get("book_id")

                if "book_id" not in updated_data or not updated_data["book_id"]:
                    self.show_message("Error", "Book ID is required for editing!", "error")
                    return

                if self.edit_book_callback:
                    self.edit_book_callback(updated_data)
                    dialog.accept()

            dialog.save_btn.clicked.connect(process_edit)
            dialog.exec()

    def on_delete_book_clicked(self, book_index):
        """Show delete confirmation and delete book"""
        if book_index < len(self.books_data):
            book_data = self.books_data[book_index]
            book_id = book_data.get("book_id")
            book_title = book_data.get("title", "this book")

            if not book_id:
                self.show_message("Error", "Book ID is missing! Cannot delete this book.", "error")
                return

            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete '{book_title}'?\n\nThis action cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                if self.delete_book_callback:
                    self.delete_book_callback(book_id)

    # Methods for Controller to call
    def update_books(self, books_data):
        """Update the books display"""
        # Store books data for later use
        self.books_data = books_data

        # Clear existing books
        while self.books_layout.count():
            item = self.books_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Update status label
        if books_data:
            self.status_label.setText(f"Showing {len(books_data)} books")
        else:
            self.status_label.setText("No books found")

        if books_data:
            # Add each book as a card
            for i, book in enumerate(books_data):
                book_card = self.create_book_card(i, book)
                self.books_layout.addWidget(book_card)
        else:
            # Show placeholder if no books
            no_books = QLabel("No books found. Click 'Add New Book' to add one.")
            no_books.setFont(QFont('Inter', 14))
            no_books.setStyleSheet('color: #9E9E9E; padding: 40px;')
            no_books.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.books_layout.addWidget(no_books)

        self.books_layout.addStretch()

    def clear_search(self):
        self.search_input.clear()

    def show_message(self, title, message, message_type="info"):
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