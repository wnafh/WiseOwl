# View/AdminMembers.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class AdminMembersView(QMainWindow):
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
        self.add_member_callback = None
        self.edit_member_callback = None
        self.search_member_callback = None
        self.delete_member_callback = None

        self.setWindowTitle("Wise Owl -- Member Management")
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
        """Pure UI setup with optimized spacing"""
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
        content_layout.setContentsMargins(35, 35, 35, 35)
        content_layout.setSpacing(0)

        # Members content
        members_content = self.create_members_content()
        content_layout.addWidget(members_content)

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
        sidebar.dashboard_callback = self.on_dashboard_clicked
        sidebar.inventory_callback = self.on_inventory_clicked
        sidebar.circulation_callback = self.on_circulation_clicked
        sidebar.members_callback = self.on_members_clicked
        sidebar.reports_callback = self.on_reports_clicked
        sidebar.settings_callback = self.on_settings_clicked
        sidebar.logout_callback = self.on_logout_clicked

        return sidebar

    def create_members_content(self):
        """Create members content with optimized layout"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header row
        header_row = QWidget()
        header_layout = QHBoxLayout(header_row)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        header = QLabel("Member Management")
        header.setFont(QFont('Karma', 32, QFont.Weight.Bold))
        header.setStyleSheet('color: #1C0C4F;')
        header_layout.addWidget(header)

        header_layout.addStretch()

        # Add Member button - BIGGER
        self.add_member_btn = QPushButton("👤  Add Member")
        self.add_member_btn.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        self.add_member_btn.setFixedHeight(50)
        self.add_member_btn.setMinimumWidth(180)
        self.add_member_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #3D8B40;
            }
        ''')
        self.add_member_btn.clicked.connect(self.on_add_member_clicked)
        header_layout.addWidget(self.add_member_btn)

        layout.addWidget(header_row)
        layout.addSpacing(12)

        subtitle = QLabel("Manage library members and view member details")
        subtitle.setFont(QFont('Inter', 15))
        subtitle.setStyleSheet('color: #596975;')
        layout.addWidget(subtitle)

        layout.addSpacing(30)

        # Search bar
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(15)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search members by name, email, or member ID...")
        self.search_input.setFont(QFont('Inter', 14))
        self.search_input.setMinimumHeight(50)
        self.search_input.setStyleSheet('''
            QLineEdit {
                padding: 0 20px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #336DED;
            }
        ''')
        self.search_input.returnPressed.connect(self.on_search_clicked)
        search_layout.addWidget(self.search_input)

        search_btn = QPushButton("🔍  Search")
        search_btn.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        search_btn.setFixedHeight(50)
        search_btn.setMinimumWidth(140)
        search_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
        ''')
        search_btn.clicked.connect(self.on_search_clicked)
        search_layout.addWidget(search_btn)

        layout.addWidget(search_widget)
        layout.addSpacing(30)

        # Members list section
        members_list_label = QLabel("Library Members")
        members_list_label.setFont(QFont('Inter', 22, QFont.Weight.Bold))
        members_list_label.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(members_list_label)

        layout.addSpacing(18)

        # Members table scroll area
        self.members_scroll = QScrollArea()
        self.members_scroll.setWidgetResizable(True)
        self.members_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.members_scroll.setStyleSheet('''
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 10px;
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

        self.members_container = QWidget()
        self.members_layout = QVBoxLayout(self.members_container)
        self.members_layout.setSpacing(18)
        self.members_layout.setContentsMargins(0, 0, 10, 0)

        # Add placeholder initially
        placeholder = QLabel(
            "No members found. Click 'Add Member' to create one\nor search to display existing members.")
        placeholder.setFont(QFont('Inter', 14))
        placeholder.setStyleSheet('color: #9E9E9E;')
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setMinimumHeight(200)
        placeholder.setWordWrap(True)
        self.members_layout.addWidget(placeholder)

        self.members_scroll.setWidget(self.members_container)
        layout.addWidget(self.members_scroll)

        return widget

    def create_member_card(self, member_data):
        """Create a member card widget - FULL WIDTH"""
        widget = QWidget()
        widget.setMinimumHeight(150)
        widget.setStyleSheet('''
            QWidget {
                background-color: white;
                border: none;
                border-radius: 6px;
            }
            QWidget:hover {
                background-color: #F0F5FF;
            }
        ''')

        layout = QHBoxLayout(widget)
        layout.setSpacing(30)
        layout.setContentsMargins(35, 25, 35, 25)

        # Avatar/Icon
        avatar_widget = QWidget()
        avatar_widget.setStyleSheet('background-color: transparent; border: none;')
        avatar_layout = QVBoxLayout(avatar_widget)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        avatar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        avatar = QLabel("👤")
        avatar.setFont(QFont('Arial', 28))
        avatar.setStyleSheet('background-color: transparent; border: none;')
        avatar_layout.addWidget(avatar)

        layout.addWidget(avatar_widget)

        # Member info
        info_widget = QWidget()
        info_widget.setStyleSheet('background-color: transparent; border: none;')
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(8)
        info_layout.setContentsMargins(0, 0, 0, 0)

        # Name and ID
        name_id_widget = QWidget()
        name_id_widget.setStyleSheet('background-color: transparent; border: none;')
        name_id_layout = QHBoxLayout(name_id_widget)
        name_id_layout.setContentsMargins(0, 0, 0, 0)
        name_id_layout.setSpacing(12)

        name_label = QLabel(member_data.get("name", "Unknown Member"))
        name_label.setFont(QFont('Inter', 17, QFont.Weight.Bold))
        name_label.setStyleSheet('color: #1C0C4F; background-color: transparent; border: none;')
        name_id_layout.addWidget(name_label)

        id_label = QLabel(f"ID: {member_data.get('member_id', 'N/A')}")
        id_label.setFont(QFont('Inter', 13))
        id_label.setStyleSheet('color: #666; background-color: transparent; border: none;')
        name_id_layout.addWidget(id_label)

        name_id_layout.addStretch()
        info_layout.addWidget(name_id_widget)

        # Email
        email_label = QLabel(f"✉️  {member_data.get('email', 'No email')}")
        email_label.setFont(QFont('Inter', 14))
        email_label.setStyleSheet('color: #596975; background-color: transparent; border: none;')
        info_layout.addWidget(email_label)

        # Stats
        stats_widget = QWidget()
        stats_widget.setStyleSheet('background-color: transparent; border: none;')
        stats_layout = QHBoxLayout(stats_widget)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(20)

        join_date = member_data.get("join_date", "N/A")
        join_label = QLabel(f"📅  Joined: {join_date}")
        join_label.setFont(QFont('Inter', 13))
        join_label.setStyleSheet('color: #757575; background-color: transparent; border: none;')
        stats_layout.addWidget(join_label)

        borrowed = member_data.get("borrowed", 0)
        borrowed_label = QLabel(f"📚  Borrowed: {borrowed}")
        borrowed_label.setFont(QFont('Inter', 13))
        borrowed_label.setStyleSheet('color: #757575; background-color: transparent; border: none;')
        stats_layout.addWidget(borrowed_label)

        overdue = member_data.get("overdue", 0)
        overdue_label = QLabel(f"⚠️  Overdue: {overdue}")
        overdue_label.setFont(QFont('Inter', 13))
        overdue_label.setStyleSheet('color: #757575; background-color: transparent; border: none;')
        stats_layout.addWidget(overdue_label)

        stats_layout.addStretch()
        info_layout.addWidget(stats_widget)

        layout.addWidget(info_widget, stretch=1)

        # Action buttons - WIDER
        actions_widget = QWidget()
        actions_widget.setStyleSheet('background-color: transparent; border: none;')
        actions_layout = QVBoxLayout(actions_widget)
        actions_layout.setSpacing(10)
        actions_layout.setContentsMargins(0, 0, 0, 0)

        # Edit button
        edit_btn = QPushButton("✏️  Edit")
        edit_btn.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        edit_btn.setFixedSize(130, 40)
        edit_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 15px;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
        ''')
        edit_btn.clicked.connect(lambda: self.on_edit_member_clicked(member_data.get("member_id", "")))
        actions_layout.addWidget(edit_btn)

        # Delete button
        delete_btn = QPushButton("🗑️  Delete")
        delete_btn.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        delete_btn.setFixedSize(130, 40)
        delete_btn.setStyleSheet('''
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 15px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        ''')
        delete_btn.clicked.connect(lambda: self.on_delete_member_clicked(member_data.get("member_id", "")))
        actions_layout.addWidget(delete_btn)

        layout.addWidget(actions_widget)

        return widget

    # ========== UI EVENT HANDLERS ==========

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
        """Handle settings click"""
        if self.settings_callback:
            self.settings_callback()
        else:
            self.show_message("Settings", "Settings feature coming soon!", "info")

    def on_logout_clicked(self):
        if self.logout_callback:
            self.logout_callback()

    def on_add_member_clicked(self):
        """Handle add member button click"""
        from View.Dialogs import AddMemberDialog

        dialog = AddMemberDialog(self)

        def process_dialog():
            member_data = dialog.get_member_data()

            # Validate data
            if not member_data.get('name'):
                self.show_message("Validation Error", "Name is required", "error")
                return

            if not member_data.get('member_id'):
                self.show_message("Validation Error", "Member ID is required", "error")
                return

            if not member_data.get('email'):
                self.show_message("Validation Error", "Email is required", "error")
                return

            # Call the callback if set
            if self.add_member_callback:
                self.add_member_callback(member_data)
                dialog.accept()
            else:
                self.show_message("Error", "Add member functionality not connected", "error")

        dialog.add_btn.clicked.connect(process_dialog)
        dialog.exec()

    def on_edit_member_clicked(self, member_id):
        """Handle edit member button click"""
        if not member_id:
            return

        # Get member info from controller
        if self.controller:
            member_info = self.controller.get_member_info(member_id)
            if not member_info:
                self.show_message("Error", "Member not found", "error")
                return

            from View.Dialogs import EditMemberDialog

            dialog = EditMemberDialog(member_info, self)

            def process_dialog():
                updated_data = dialog.get_updated_data()

                # Validate data
                if not updated_data.get('name'):
                    self.show_message("Validation Error", "Name is required", "error")
                    return

                if not updated_data.get('email'):
                    self.show_message("Validation Error", "Email is required", "error")
                    return

                # Call the callback if set
                if self.edit_member_callback:
                    self.edit_member_callback(member_id, updated_data)
                    dialog.accept()
                else:
                    self.show_message("Error", "Edit functionality not connected", "error")

            dialog.save_btn.clicked.connect(process_dialog)
            dialog.exec()
        else:
            self.show_message("Error", "Controller not connected", "error")

    def on_delete_member_clicked(self, member_id):
        """Handle delete member button click"""
        if self.delete_member_callback:
            self.delete_member_callback(member_id)
        else:
            self.show_message("Error", "Delete functionality not connected", "error")

    def on_search_clicked(self):
        """Handle search button click"""
        query = self.search_input.text().strip()
        if self.search_member_callback:
            self.search_member_callback(query)
        else:
            self.show_message("Error", "Search functionality not connected", "error")

    # ========== PUBLIC METHODS ==========

    def update_members_list(self, members_data):
        """Update the members list display"""
        # Clear existing members
        while self.members_layout.count():
            item = self.members_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not members_data:
            # Show empty state
            placeholder = QLabel(
                "No members found.\n\nClick 'Add Member' to create one or search to display existing members.")
            placeholder.setFont(QFont('Inter', 14))
            placeholder.setStyleSheet('color: #9E9E9E;')
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setMinimumHeight(200)
            placeholder.setWordWrap(True)
            self.members_layout.addWidget(placeholder)
            return

        # Add each member as a card
        for member in members_data:
            member_card = self.create_member_card(member)
            self.members_layout.addWidget(member_card)

        # Add stretch at the end
        self.members_layout.addStretch()

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