# View/AdminCirculation.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class AdminCirculationView(QMainWindow):
    def __init__(self, user_name, member_id, role):
        super().__init__()
        self.user_name = user_name
        self.member_id = member_id
        self.role = role

        self.controller = None

        # Initialize all callback references
        self.dashboard_callback = None
        self.inventory_callback = None
        self.circulation_callback = None
        self.members_callback = None
        self.reports_callback = None
        self.logout_callback = None
        self.checkout_callback = None
        self.checkin_callback = None

        self.setWindowTitle("Wise Owl -- Circulation")
        try:
            self.setWindowIcon(QIcon('View/LOGO3.png'))
        except:
            pass

        # Optimized window sizing
        self.setMinimumSize(1280, 720)
        self.resize(1440, 900)

        self.setup_ui()
        self.center()

    def setup_ui(self):
        """Pure UI setup with minimal spacing"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # Content
        content_widget = QWidget()
        content_widget.setStyleSheet('background-color: #F5F5F5;')
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Header
        header = QLabel("Circulation Management")
        header.setFont(QFont('Karma', 28, QFont.Weight.Bold))
        header.setStyleSheet('color: #1C0C4F;')
        content_layout.addWidget(header)

        subtitle = QLabel("Process book borrowing and returns")
        subtitle.setFont(QFont('Inter', 14))
        subtitle.setStyleSheet('color: #596975;')
        content_layout.addWidget(subtitle)

        # Two-column layout
        columns_widget = QWidget()
        columns_layout = QHBoxLayout(columns_widget)
        columns_layout.setSpacing(20)
        columns_layout.setContentsMargins(0, 0, 0, 0)

        # Left: Forms
        left_col = self.create_circulation_content()
        columns_layout.addWidget(left_col, stretch=3)

        # Right: Stats - NO BOX
        right_col = self.create_stats_sidebar()
        columns_layout.addWidget(right_col, stretch=2)

        content_layout.addWidget(columns_widget)
        content_layout.addStretch()

        main_layout.addWidget(content_widget, stretch=1)

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

    def create_sidebar(self):
        """Create sidebar with logo"""
        from View.AdminSidebar import AdminSidebarView

        sidebar = AdminSidebarView(self.user_name, self.member_id, self.role)

        # Set up sidebar callbacks
        sidebar.dashboard_callback = self.on_dashboard_clicked
        sidebar.inventory_callback = self.on_inventory_clicked
        sidebar.circulation_callback = self.on_circulation_clicked
        sidebar.members_callback = self.on_members_clicked
        sidebar.reports_callback = self.on_reports_clicked
        sidebar.logout_callback = self.on_logout_clicked

        return sidebar

    def create_circulation_content(self):
        """Create circulation forms without any boxes"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)

        checkout_section = self.create_checkout_section()
        layout.addWidget(checkout_section)

        checkin_section = self.create_checkin_section()
        layout.addWidget(checkin_section)

        layout.addStretch()

        return widget

    def create_checkout_section(self):
        """Create checkout section with book title input"""
        widget = QWidget()

        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        # Check Out Book header
        header = QLabel("📤 Check Out Book")
        header.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        header.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(header)

        # Process book borrowing for members text
        desc = QLabel("Process book borrowing for members")
        desc.setFont(QFont('Inter', 13))
        desc.setStyleSheet('color: #596975;')
        layout.addWidget(desc)

        # Member ID section
        member_label = QLabel("Member ID")
        member_label.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        member_label.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(member_label)

        self.member_input = QLineEdit()
        self.member_input.setPlaceholderText("Enter member ID (e.g., 202501)")
        self.member_input.setFont(QFont('Inter', 13))
        self.member_input.setFixedHeight(40)
        self.member_input.setStyleSheet('''
            QLineEdit {
                padding: 0 14px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #336DED;
            }
        ''')
        layout.addWidget(self.member_input)

        # Book Title section
        book_label = QLabel("Book Title")
        book_label.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        book_label.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(book_label)

        self.book_title_out_input = QLineEdit()
        self.book_title_out_input.setPlaceholderText("Enter book title")
        self.book_title_out_input.setFont(QFont('Inter', 13))
        self.book_title_out_input.setFixedHeight(40)
        self.book_title_out_input.setStyleSheet('''
            QLineEdit {
                padding: 0 14px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #336DED;
            }
        ''')
        layout.addWidget(self.book_title_out_input)

        # Button
        checkout_btn = QPushButton("✅ Check Out Book")
        checkout_btn.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        checkout_btn.setFixedHeight(45)
        checkout_btn.setStyleSheet('''
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
        checkout_btn.clicked.connect(self.on_checkout_clicked)
        layout.addWidget(checkout_btn)

        return widget

    def create_checkin_section(self):
        """Create checkin section with member ID and book title"""
        widget = QWidget()

        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        # Check In Book header
        header = QLabel("📥 Check In Book")
        header.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        header.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(header)

        # Process book returns text
        desc = QLabel("Process book returns")
        desc.setFont(QFont('Inter', 13))
        desc.setStyleSheet('color: #596975;')
        layout.addWidget(desc)

        # Member ID section
        member_label = QLabel("Member ID")
        member_label.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        member_label.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(member_label)

        self.member_in_input = QLineEdit()
        self.member_in_input.setPlaceholderText("Enter member ID: ")
        self.member_in_input.setFont(QFont('Inter', 13))
        self.member_in_input.setFixedHeight(40)
        self.member_in_input.setStyleSheet('''
            QLineEdit {
                padding: 0 14px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #336DED;
            }
        ''')
        layout.addWidget(self.member_in_input)

        # Book Title section
        book_label = QLabel("Book Title")
        book_label.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        book_label.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(book_label)

        self.book_title_in_input = QLineEdit()
        self.book_title_in_input.setPlaceholderText("Enter book title")
        self.book_title_in_input.setFont(QFont('Inter', 13))
        self.book_title_in_input.setFixedHeight(40)
        self.book_title_in_input.setStyleSheet('''
            QLineEdit {
                padding: 0 14px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #336DED;
            }
        ''')
        layout.addWidget(self.book_title_in_input)

        # Book Condition section
        condition_label = QLabel("Book Condition")
        condition_label.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        condition_label.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(condition_label)

        self.condition_combo = QComboBox()
        self.condition_combo.addItems(["Good", "Fair", "Poor", "Damaged"])
        self.condition_combo.setFont(QFont('Inter', 13))
        self.condition_combo.setFixedHeight(40)
        self.condition_combo.setStyleSheet('''
            QComboBox {
                padding: 0 14px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                background-color: white;
            }
            QComboBox:hover {
                border-color: #336DED;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
        ''')
        layout.addWidget(self.condition_combo)

        # Button
        checkin_btn = QPushButton("✅ Check In Book")
        checkin_btn.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        checkin_btn.setFixedHeight(45)
        checkin_btn.setStyleSheet('''
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
        checkin_btn.clicked.connect(self.on_checkin_clicked)
        layout.addWidget(checkin_btn)

        return widget

    def create_stats_sidebar(self):
        """Create stats sidebar WITHOUT box"""
        widget = QWidget()
        widget.setStyleSheet('background-color: transparent;')

        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        # Library Statistics header
        header = QLabel("Library Statistics")
        header.setFont(QFont('Inter', 20, QFont.Weight.Bold))
        header.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(header)

        # Stats display - NO BOXES
        self.stats_container = QWidget()
        self.stats_layout = QVBoxLayout(self.stats_container)
        self.stats_layout.setSpacing(16)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stats_container)

        layout.addStretch()

        return widget

    # CALLBACK METHODS

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

    def on_logout_clicked(self):
        if self.logout_callback:
            self.logout_callback()

    def on_checkout_clicked(self):
        member_id = self.member_input.text().strip()
        book_title = self.book_title_out_input.text().strip()

        if not member_id:
            self.show_message("Validation Error", "Please enter the Member ID.", "warning")
            return

        if not book_title:
            self.show_message("Validation Error", "Please enter the book title.", "warning")
            return

        if self.checkout_callback:
            # The callback now handles showing the receipt internally
            self.checkout_callback(member_id, book_title)

    def on_checkin_clicked(self):
        member_id = self.member_in_input.text().strip()
        book_title = self.book_title_in_input.text().strip()
        condition = self.condition_combo.currentText()

        if not member_id:
            self.show_message("Validation Error", "Please enter the Member ID returning the book.", "warning")
            return

        if not book_title:
            self.show_message("Validation Error", "Please enter the book title.", "warning")
            return

        print(f"Checkin - Member: {member_id}, Book Title: {book_title}, Condition: {condition}")  # DEBUG
        print(f"Checkin callback exists: {self.checkin_callback is not None}")  # DEBUG

        if self.checkin_callback:
            self.checkin_callback(member_id, book_title, condition)
        else:
            print("ERROR: checkin_callback is not set!")
            self.show_message("Error", "Checkin function not available", "error")

    # METHODS FOR CONTROLLER

    def update_stats(self, stats_data):
        """Update statistics display - NO BOXES"""
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Define consistent styling for each stat type
        stat_configs = {
            "Total Books": {"color": "#336DED", "icon": "📚"},
            "Available": {"color": "#4CAF50", "icon": "✅"},
            "Borrowed": {"color": "#FF9800", "icon": "📖"},
            "Total Members": {"color": "#9C27B0", "icon": "👥"}
        }

        # Create and add stat items - CLEAN TEXT, NO BOXES
        for stat in stats_data:
            title = stat["title"]
            config = stat_configs.get(title, {"color": "#1C0C4F", "icon": ""})

            # Create a widget for each stat
            stat_widget = QWidget()
            stat_layout = QVBoxLayout(stat_widget)
            stat_layout.setSpacing(4)
            stat_layout.setContentsMargins(0, 0, 0, 0)

            # Value with icon - CLEAN TEXT
            value_widget = QWidget()
            value_layout = QHBoxLayout(value_widget)
            value_layout.setContentsMargins(0, 0, 0, 0)
            value_layout.setSpacing(8)
            value_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            if config["icon"]:
                icon_label = QLabel(config["icon"])
                icon_label.setFont(QFont('Arial', 20))
                icon_label.setStyleSheet(f'color: {config["color"]};')
                value_layout.addWidget(icon_label)

            value_label = QLabel(str(stat["value"]))
            value_label.setFont(QFont('Inter', 28, QFont.Weight.Bold))
            value_label.setStyleSheet(f'color: {config["color"]};')
            value_layout.addWidget(value_label)

            value_layout.addStretch()
            stat_layout.addWidget(value_widget)

            # Title - CLEAN TEXT
            title_label = QLabel(title)
            title_label.setFont(QFont('Inter', 12))
            title_label.setStyleSheet('color: #596975;')
            stat_layout.addWidget(title_label)

            self.stats_layout.addWidget(stat_widget)

    def show_receipt(self, receipt_data, librarian_name=None, librarian_id=None):
        """Show checkout receipt dialog with librarian info"""
        from View.Dialogs import CheckoutReceiptDialog

        receipt_dialog = CheckoutReceiptDialog(receipt_data, self, librarian_name, librarian_id)
        receipt_dialog.exec()

    def show_checkin_receipt(self, checkin_data):
        """Show checkin receipt dialog"""
        from View.Dialogs import CheckinReceiptDialog

        receipt_dialog = CheckinReceiptDialog(checkin_data, self)
        receipt_dialog.exec()

    def clear_checkout_form(self):
        self.member_input.clear()
        self.book_title_out_input.clear()

    def clear_checkin_form(self):
        self.member_in_input.clear()
        self.book_title_in_input.clear()
        self.condition_combo.setCurrentIndex(0)

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