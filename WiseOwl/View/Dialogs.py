# View/Dialogs.py
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class AddBookDialog(QDialog):
    """Dialog for adding a new book"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Book")
        self.setMinimumSize(500, 550)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        self.title_label = QLabel("Title:*")
        self.title_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter book title")
        self.title_input.setMinimumHeight(40)
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)

        # Author
        self.author_label = QLabel("Author:*")
        self.author_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Enter author name")
        self.author_input.setMinimumHeight(40)
        layout.addWidget(self.author_label)
        layout.addWidget(self.author_input)

        # Genre
        self.genre_label = QLabel("Genre:")
        self.genre_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("e.g., Fiction, Science, Romance")
        self.genre_input.setMinimumHeight(40)
        layout.addWidget(self.genre_label)
        layout.addWidget(self.genre_input)

        # Total Copies
        self.copies_label = QLabel("Total Copies:*")
        self.copies_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.copies_input = QSpinBox()
        self.copies_input.setMinimum(1)
        self.copies_input.setMaximum(1000)
        self.copies_input.setValue(1)
        self.copies_input.setMinimumHeight(40)
        layout.addWidget(self.copies_label)
        layout.addWidget(self.copies_input)

        # Location
        self.location_label = QLabel("Location:")
        self.location_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("e.g., Shelf A1, Fiction B2")
        self.location_input.setMinimumHeight(40)
        layout.addWidget(self.location_label)
        layout.addWidget(self.location_input)

        # Description
        self.desc_label = QLabel("Description:")
        self.desc_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        self.desc_input.setPlaceholderText("Enter book description (optional)")
        layout.addWidget(self.desc_label)
        layout.addWidget(self.desc_input)

        # Required fields note
        required_note = QLabel("* Required fields")
        required_note.setFont(QFont('Inter', 10))
        required_note.setStyleSheet('color: #F44336; margin-top: 10px;')
        layout.addWidget(required_note)

        # Buttons
        buttons_layout = QHBoxLayout()

        self.add_btn = QPushButton("Add Book")
        self.add_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.add_btn.setMinimumHeight(45)
        self.add_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3D8B40;
            }
        ''')
        buttons_layout.addWidget(self.add_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.cancel_btn.setMinimumHeight(45)
        self.cancel_btn.setStyleSheet('''
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        ''')
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_btn)

        layout.addLayout(buttons_layout)

    def get_book_data(self):
        """Get the book data from the form"""
        return {
            "title": self.title_input.text().strip(),
            "author": self.author_input.text().strip(),
            "genre": self.genre_input.text().strip(),
            "total_copies": self.copies_input.value(),
            "location": self.location_input.text().strip(),
            "description": self.desc_input.toPlainText().strip()
        }

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
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes


class AddMemberDialog(QDialog):
    """Dialog for adding a new member"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Member")
        self.setMinimumSize(400, 400)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Name
        self.name_label = QLabel("Full Name:*")
        self.name_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter member's full name")
        self.name_input.setMinimumHeight(40)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        # Member ID
        self.member_id_label = QLabel("Member ID:*")
        self.member_id_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.member_id_input = QLineEdit()
        self.member_id_input.setPlaceholderText("Enter unique member ID")
        self.member_id_input.setMinimumHeight(40)
        layout.addWidget(self.member_id_label)
        layout.addWidget(self.member_id_input)

        # Email
        self.email_label = QLabel("Email:*")
        self.email_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        self.email_input.setMinimumHeight(40)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        # Phone
        self.phone_label = QLabel("Phone:")
        self.phone_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number (optional)")
        self.phone_input.setMinimumHeight(40)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)

        # Required fields note
        required_note = QLabel("* Required fields")
        required_note.setFont(QFont('Inter', 10))
        required_note.setStyleSheet('color: #F44336; margin-top: 10px;')
        layout.addWidget(required_note)

        # Buttons
        buttons_layout = QHBoxLayout()

        self.add_btn = QPushButton("Add Member")
        self.add_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.add_btn.setMinimumHeight(45)
        self.add_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3D8B40;
            }
        ''')
        buttons_layout.addWidget(self.add_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.cancel_btn.setMinimumHeight(45)
        self.cancel_btn.setStyleSheet('''
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        ''')
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_btn)

        layout.addLayout(buttons_layout)

    def get_member_data(self):
        """Get the member data from the form"""
        return {
            "name": self.name_input.text().strip(),
            "member_id": self.member_id_input.text().strip(),
            "email": self.email_input.text().strip(),
            "phone": self.phone_input.text().strip()
        }

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
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes


class EditBookDialog(QDialog):
    """Dialog for editing a book"""

    def __init__(self, book_title, current_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit Book: {book_title}")
        self.setMinimumSize(500, 550)
        self.current_data = current_data or {}

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        self.title_label = QLabel("Title:*")
        self.title_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.title_input = QLineEdit()
        self.title_input.setText(self.current_data.get("title", ""))
        self.title_input.setPlaceholderText("Enter book title")
        self.title_input.setMinimumHeight(40)
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)

        # Author
        self.author_label = QLabel("Author:*")
        self.author_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.author_input = QLineEdit()
        self.author_input.setText(self.current_data.get("author", ""))
        self.author_input.setPlaceholderText("Enter author name")
        self.author_input.setMinimumHeight(40)
        layout.addWidget(self.author_label)
        layout.addWidget(self.author_input)

        # Genre
        self.genre_label = QLabel("Genre:")
        self.genre_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.genre_input = QLineEdit()
        self.genre_input.setText(self.current_data.get("genre", ""))
        self.genre_input.setPlaceholderText("e.g., Fiction, Science, Romance")
        self.genre_input.setMinimumHeight(40)
        layout.addWidget(self.genre_label)
        layout.addWidget(self.genre_input)

        # Total Copies
        self.copies_label = QLabel("Total Copies:*")
        self.copies_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.copies_input = QSpinBox()
        self.copies_input.setMinimum(1)
        self.copies_input.setMaximum(1000)
        self.copies_input.setValue(self.current_data.get("total_copies", 1))
        self.copies_input.setMinimumHeight(40)
        layout.addWidget(self.copies_label)
        layout.addWidget(self.copies_input)

        # Available Copies
        self.available_label = QLabel("Available Copies:*")
        self.available_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.available_input = QSpinBox()
        self.available_input.setMinimum(0)
        self.available_input.setMaximum(self.copies_input.value())
        self.available_input.setValue(self.current_data.get("available_copies", 1))
        self.available_input.setMinimumHeight(40)
        layout.addWidget(self.available_label)
        layout.addWidget(self.available_input)

        # Connect copies change to update available maximum
        self.copies_input.valueChanged.connect(
            lambda: self.available_input.setMaximum(self.copies_input.value())
        )

        # Location
        self.location_label = QLabel("Location:")
        self.location_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.location_input = QLineEdit()
        self.location_input.setText(self.current_data.get("location", ""))
        self.location_input.setPlaceholderText("e.g., Shelf A1, Fiction B2")
        self.location_input.setMinimumHeight(40)
        layout.addWidget(self.location_label)
        layout.addWidget(self.location_input)

        # Description
        self.desc_label = QLabel("Description:")
        self.desc_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        self.desc_input.setText(self.current_data.get("description", ""))
        self.desc_input.setPlaceholderText("Enter book description (optional)")
        layout.addWidget(self.desc_label)
        layout.addWidget(self.desc_input)

        # Required fields note
        required_note = QLabel("* Required fields")
        required_note.setFont(QFont('Inter', 10))
        required_note.setStyleSheet('color: #F44336; margin-top: 10px;')
        layout.addWidget(required_note)

        # Buttons
        buttons_layout = QHBoxLayout()

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.save_btn.setMinimumHeight(45)
        self.save_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
        ''')
        buttons_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.cancel_btn.setMinimumHeight(45)
        self.cancel_btn.setStyleSheet('''
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        ''')
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_btn)

        layout.addLayout(buttons_layout)

    def get_updated_data(self):
        """Get the updated book data from the form"""
        return {
            "title": self.title_input.text().strip(),
            "author": self.author_input.text().strip(),
            "genre": self.genre_input.text().strip(),
            "total_copies": self.copies_input.value(),
            "available_copies": self.available_input.value(),
            "location": self.location_input.text().strip(),
            "description": self.desc_input.toPlainText().strip()
        }

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
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes


class EditMemberDialog(QDialog):
    """Dialog for editing a member"""

    def __init__(self, member_data, parent=None):
        super().__init__(parent)
        self.member_data = member_data
        self.setWindowTitle(f"Edit Member: {member_data.get('name', '')}")
        self.setModal(True)
        self.setMinimumSize(500, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Edit Member")
        title.setFont(QFont('Inter', 20, QFont.Weight.Bold))
        title.setStyleSheet('color: #1C0C4F;')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Form
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        # Member ID (read-only)
        member_id_label = QLabel("Member ID:")
        member_id_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        member_id_value = QLabel(self.member_data.get("member_id", ""))
        member_id_value.setFont(QFont('Inter', 12))
        member_id_value.setStyleSheet("color: #666;")
        form_layout.addRow(member_id_label, member_id_value)

        # Name
        self.name_label = QLabel("Full Name:*")
        self.name_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.name_input = QLineEdit()
        self.name_input.setText(self.member_data.get("name", ""))
        self.name_input.setPlaceholderText("Enter full name")
        self.name_input.setFont(QFont('Inter', 12))
        form_layout.addRow(self.name_label, self.name_input)

        # Email
        self.email_label = QLabel("Email:*")
        self.email_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.email_input = QLineEdit()
        self.email_input.setText(self.member_data.get("email", ""))
        self.email_input.setPlaceholderText("Enter email address")
        self.email_input.setFont(QFont('Inter', 12))
        form_layout.addRow(self.email_label, self.email_input)

        # Phone
        self.phone_label = QLabel("Phone:")
        self.phone_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.phone_input = QLineEdit()
        self.phone_input.setText(self.member_data.get("phone", ""))
        self.phone_input.setPlaceholderText("Enter phone number")
        self.phone_input.setFont(QFont('Inter', 12))
        form_layout.addRow(self.phone_label, self.phone_input)

        # Address
        self.address_label = QLabel("Address:")
        self.address_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        self.address_input.setText(self.member_data.get("address", ""))
        self.address_input.setPlaceholderText("Enter address")
        self.address_input.setFont(QFont('Inter', 12))
        form_layout.addRow(self.address_label, self.address_input)

        # Membership Status
        self.status_label = QLabel("Status:")
        self.status_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Active", "Inactive", "Suspended"])
        self.status_combo.setCurrentText(self.member_data.get("status", "Active"))
        self.status_combo.setFont(QFont('Inter', 12))
        form_layout.addRow(self.status_label, self.status_combo)

        # Required fields note
        required_note = QLabel("* Required fields")
        required_note.setFont(QFont('Inter', 10))
        required_note.setStyleSheet('color: #F44336; margin-top: 10px;')
        layout.addWidget(required_note)
        layout.addWidget(form_widget)
        layout.addStretch()

        # Buttons
        buttons_layout = QHBoxLayout()

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.save_btn.setFixedHeight(45)
        self.save_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3D8B40;
            }
        ''')
        buttons_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.cancel_btn.setFixedHeight(45)
        self.cancel_btn.setStyleSheet('''
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        ''')
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_btn)

        layout.addLayout(buttons_layout)

    def get_updated_data(self):
        """Get the updated member data from the form"""
        return {
            "member_id": self.member_data.get("member_id", ""),
            "name": self.name_input.text().strip(),
            "email": self.email_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "address": self.address_input.toPlainText().strip(),
            "status": self.status_combo.currentText()
        }

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
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes


class ViewMemberDialog(QDialog):
    """Dialog for viewing member details"""

    def __init__(self, member_data, parent=None):
        super().__init__(parent)
        self.member_data = member_data
        self.setWindowTitle(f"Member Details: {member_data.get('name', '')}")
        self.setModal(True)
        self.setMinimumSize(500, 500)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Member Details")
        title.setFont(QFont('Inter', 20, QFont.Weight.Bold))
        title.setStyleSheet('color: #1C0C4F;')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Member info in a card-like layout
        info_widget = QWidget()
        info_widget.setStyleSheet('''
            QWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
                padding: 20px;
            }
        ''')
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(15)

        # Name and ID section
        name_section = QWidget()
        name_layout = QHBoxLayout(name_section)
        name_layout.setContentsMargins(0, 0, 0, 0)

        name_icon = QLabel("👤")
        name_icon.setFont(QFont('Inter', 24))
        name_layout.addWidget(name_icon)

        name_text = QLabel(self.member_data.get("name", "Unknown"))
        name_text.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        name_text.setStyleSheet('color: #1C0C4F;')
        name_layout.addWidget(name_text)

        id_label = QLabel(f"ID: {self.member_data.get('member_id', 'N/A')}")
        id_label.setFont(QFont('Inter', 12))
        id_label.setStyleSheet('color: #666; background-color: #F0F0F0; padding: 4px 12px; border-radius: 6px;')
        name_layout.addWidget(id_label)

        name_layout.addStretch()
        info_layout.addWidget(name_section)

        # Info grid
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(12)
        grid_layout.setColumnStretch(1, 1)

        # Email
        email_label = QLabel("Email:")
        email_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        email_label.setStyleSheet('color: #666;')
        email_value = QLabel(self.member_data.get("email", "N/A"))
        email_value.setFont(QFont('Inter', 12))
        grid_layout.addWidget(email_label, 0, 0)
        grid_layout.addWidget(email_value, 0, 1)

        # Phone
        phone_label = QLabel("Phone:")
        phone_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        phone_label.setStyleSheet('color: #666;')
        phone_value = QLabel(self.member_data.get("phone", "N/A"))
        phone_value.setFont(QFont('Inter', 12))
        grid_layout.addWidget(phone_label, 1, 0)
        grid_layout.addWidget(phone_value, 1, 1)

        # Join Date
        join_label = QLabel("Join Date:")
        join_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        join_label.setStyleSheet('color: #666;')
        join_value = QLabel(self.member_data.get("join_date", "N/A"))
        join_value.setFont(QFont('Inter', 12))
        grid_layout.addWidget(join_label, 2, 0)
        grid_layout.addWidget(join_value, 2, 1)

        # Borrowed Count
        borrowed_label = QLabel("Books Borrowed:")
        borrowed_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        borrowed_label.setStyleSheet('color: #666;')
        borrowed_value = QLabel(str(self.member_data.get("borrowed", 0)))
        borrowed_value.setFont(QFont('Inter', 12))
        grid_layout.addWidget(borrowed_label, 3, 0)
        grid_layout.addWidget(borrowed_value, 3, 1)

        # Overdue Count
        overdue_label = QLabel("Overdue Books:")
        overdue_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        overdue_label.setStyleSheet('color: #666;')
        overdue_value = QLabel(str(self.member_data.get("overdue", 0)))
        overdue_value.setFont(QFont('Inter', 12))
        overdue_value.setStyleSheet('color: #F44336;' if self.member_data.get("overdue", 0) > 0 else 'color: #666;')
        grid_layout.addWidget(overdue_label, 4, 0)
        grid_layout.addWidget(overdue_value, 4, 1)

        info_layout.addWidget(grid_widget)

        # Address section (if available)
        if self.member_data.get("address"):
            address_label = QLabel("Address:")
            address_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
            address_label.setStyleSheet('color: #666; margin-top: 10px;')
            info_layout.addWidget(address_label)

            address_value = QLabel(self.member_data.get("address", ""))
            address_value.setFont(QFont('Inter', 12))
            address_value.setWordWrap(True)
            address_value.setStyleSheet('color: #333; background-color: #F9F9F9; padding: 10px; border-radius: 6px;')
            info_layout.addWidget(address_value)

        # Status
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 10, 0, 0)

        status_label = QLabel("Status:")
        status_label.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        status_label.setStyleSheet('color: #666;')
        status_layout.addWidget(status_label)

        status_value = QLabel(self.member_data.get("status", "Active"))
        status_value.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        status_color = "#4CAF50" if self.member_data.get("status") == "Active" else "#F44336"
        status_value.setStyleSheet(
            f'color: white; background-color: {status_color}; padding: 4px 12px; border-radius: 6px;')
        status_layout.addWidget(status_value)

        status_layout.addStretch()
        info_layout.addWidget(status_widget)

        layout.addWidget(info_widget)
        layout.addStretch()

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        close_btn.setFixedHeight(45)
        close_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
        ''')
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

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
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes


class ConfirmationDialog(QDialog):
    """Simple confirmation dialog"""

    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumSize(400, 200)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Message
        message_label = QLabel(message)
        message_label.setFont(QFont('Inter', 13))
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message_label)

        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.yes_btn = QPushButton("Yes")
        self.yes_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.yes_btn.setFixedHeight(40)
        self.yes_btn.setFixedWidth(100)
        self.yes_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3D8B40;
            }
        ''')
        buttons_layout.addWidget(self.yes_btn)

        self.no_btn = QPushButton("No")
        self.no_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.no_btn.setFixedHeight(40)
        self.no_btn.setFixedWidth(100)
        self.no_btn.setStyleSheet('''
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        ''')
        self.no_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.no_btn)

        layout.addLayout(buttons_layout)

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
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes


class CheckoutReceiptDialog(QDialog):
    def __init__(self, checkout_data, parent=None, librarian_name=None, librarian_id=None):
        super().__init__(parent)
        self.checkout_data = checkout_data
        self.librarian_name = librarian_name
        self.librarian_id = librarian_id
        self.setWindowTitle("Checkout Receipt")
        self.setModal(True)
        self.setMinimumSize(450, 600)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)

        self.setup_ui()

    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area for content (in case receipt is long)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        # Container for receipt
        self.container = QWidget()  # Make container accessible for PDF export
        self.container.setStyleSheet("background-color: white;")

        receipt_layout = QVBoxLayout(self.container)
        receipt_layout.setSpacing(15)
        receipt_layout.setContentsMargins(30, 30, 30, 30)

        # Header with logo/store name
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(5)

        # Store name
        store_name = QLabel("WISE OWL LIBRARY")
        store_name.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        store_name.setStyleSheet('color: #1C0C4F;')
        store_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(store_name)

        # Receipt title
        receipt_title = QLabel("📋 CHECKOUT RECEIPT")
        receipt_title.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        receipt_title.setStyleSheet('color: #336DED; letter-spacing: 1px;')
        receipt_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(receipt_title)

        # Divider
        divider1 = QFrame()
        divider1.setFrameShape(QFrame.Shape.HLine)
        divider1.setFrameShadow(QFrame.Shadow.Sunken)
        divider1.setStyleSheet("background-color: #E0E0E0; max-height: 1px;")
        header_layout.addWidget(divider1)

        receipt_layout.addWidget(header_widget)

        # Date and time
        datetime_widget = QWidget()
        datetime_layout = QHBoxLayout(datetime_widget)
        datetime_layout.setContentsMargins(0, 0, 0, 0)

        current_time = QDateTime.currentDateTime()
        date_str = current_time.toString("MMM dd, yyyy")
        time_str = current_time.toString("hh:mm AP")

        date_label = QLabel(f"Date: {date_str}")
        date_label.setFont(QFont('Inter', 11))
        date_label.setStyleSheet('color: #666;')

        time_label = QLabel(f"Time: {time_str}")
        time_label.setFont(QFont('Inter', 11))
        time_label.setStyleSheet('color: #666;')

        datetime_layout.addWidget(date_label)
        datetime_layout.addStretch()
        datetime_layout.addWidget(time_label)

        receipt_layout.addWidget(datetime_widget)

        if self.librarian_name:
            librarian_header = QLabel("👨‍💼 PROCESSED BY")
            librarian_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
            librarian_header.setStyleSheet('color: #1C0C4F; padding-bottom: 5px;')
            receipt_layout.addWidget(librarian_header)

            librarian_grid = QWidget()
            librarian_grid_layout = QGridLayout(librarian_grid)
            librarian_grid_layout.setContentsMargins(10, 0, 0, 0)
            librarian_grid_layout.setVerticalSpacing(8)
            librarian_grid_layout.setHorizontalSpacing(15)

            # Librarian Name
            librarian_icon = QLabel("👤")
            librarian_icon.setFont(QFont('Inter', 11))
            librarian_grid_layout.addWidget(librarian_icon, 0, 0)

            librarian_label = QLabel("Librarian:")
            librarian_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
            librarian_label.setStyleSheet('color: #666;')
            librarian_grid_layout.addWidget(librarian_label, 0, 1)

            librarian_value = QLabel(self.librarian_name)
            librarian_value.setFont(QFont('Inter', 10))
            librarian_grid_layout.addWidget(librarian_value, 0, 2)

            # Librarian ID
            librarian_id_icon = QLabel("🆔")
            librarian_id_icon.setFont(QFont('Inter', 11))
            librarian_grid_layout.addWidget(librarian_id_icon, 1, 0)

            librarian_id_label = QLabel("Staff ID:")
            librarian_id_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
            librarian_id_label.setStyleSheet('color: #666;')
            librarian_grid_layout.addWidget(librarian_id_label, 1, 1)

            librarian_id_value = QLabel(self.librarian_id or 'N/A')
            librarian_id_value.setFont(QFont('Inter', 10))
            librarian_grid_layout.addWidget(librarian_id_value, 1, 2)

            librarian_grid_layout.setColumnStretch(2, 1)
            receipt_layout.addWidget(librarian_grid)

            # Divider
            divider2 = QFrame()
            divider2.setFrameShape(QFrame.Shape.HLine)
            divider2.setStyleSheet("background-color: #E0E0E0; max-height: 1px; margin: 5px 0;")
            receipt_layout.addWidget(divider2)

        # Combined information card
        info_card = QWidget()
        info_card.setStyleSheet('''
            QWidget {
                background-color: #F8F9FA;
                border-radius: 8px;
                padding: 15px;
                margin-top: 5px;
            }
        ''')
        info_layout = QVBoxLayout(info_card)
        info_layout.setSpacing(12)

        # Member Information Section (within card)
        member_header = QLabel("👤 MEMBER INFORMATION")
        member_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        member_header.setStyleSheet('color: #1C0C4F; padding-bottom: 5px;')
        info_layout.addWidget(member_header)

        # Member details grid
        member_grid = QWidget()
        member_grid_layout = QGridLayout(member_grid)
        member_grid_layout.setContentsMargins(10, 0, 0, 0)
        member_grid_layout.setVerticalSpacing(8)
        member_grid_layout.setHorizontalSpacing(15)

        # Member Name
        name_icon = QLabel("👤")
        name_icon.setFont(QFont('Inter', 11))
        member_grid_layout.addWidget(name_icon, 0, 0)

        name_label = QLabel("Name:")
        name_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        name_label.setStyleSheet('color: #666;')
        member_grid_layout.addWidget(name_label, 0, 1)

        name_value = QLabel(self.checkout_data.get('member_name', 'N/A'))
        name_value.setFont(QFont('Inter', 10))
        member_grid_layout.addWidget(name_value, 0, 2)

        # Member ID
        id_icon = QLabel("🆔")
        id_icon.setFont(QFont('Inter', 11))
        member_grid_layout.addWidget(id_icon, 1, 0)

        id_label = QLabel("Member ID:")
        id_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        id_label.setStyleSheet('color: #666;')
        member_grid_layout.addWidget(id_label, 1, 1)

        id_value = QLabel(self.checkout_data.get('member_id', 'N/A'))
        id_value.setFont(QFont('Inter', 10))
        member_grid_layout.addWidget(id_value, 1, 2)

        member_grid_layout.setColumnStretch(2, 1)
        info_layout.addWidget(member_grid)

        # Divider
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.Shape.HLine)
        divider2.setStyleSheet("background-color: #E0E0E0; max-height: 1px; margin: 5px 0;")
        info_layout.addWidget(divider2)

        # Book Information Section (within card)
        book_header = QLabel("📚 BOOK INFORMATION")
        book_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        book_header.setStyleSheet('color: #336DED; padding-bottom: 5px;')
        info_layout.addWidget(book_header)

        # Book details grid
        book_grid = QWidget()
        book_grid_layout = QGridLayout(book_grid)
        book_grid_layout.setContentsMargins(10, 0, 0, 0)
        book_grid_layout.setVerticalSpacing(8)
        book_grid_layout.setHorizontalSpacing(15)

        # Book Title
        title_icon = QLabel("📖")
        title_icon.setFont(QFont('Inter', 11))
        book_grid_layout.addWidget(title_icon, 0, 0)

        title_label = QLabel("Title:")
        title_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        title_label.setStyleSheet('color: #666;')
        book_grid_layout.addWidget(title_label, 0, 1)

        title_value = QLabel(self.checkout_data.get('book_title', 'N/A'))
        title_value.setFont(QFont('Inter', 10))
        title_value.setWordWrap(True)
        book_grid_layout.addWidget(title_value, 0, 2)

        # Book ID
        book_id_icon = QLabel("🔖")
        book_id_icon.setFont(QFont('Inter', 11))
        book_grid_layout.addWidget(book_id_icon, 1, 0)

        book_id_label = QLabel("Book ID:")
        book_id_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        book_id_label.setStyleSheet('color: #666;')
        book_grid_layout.addWidget(book_id_label, 1, 1)

        book_id_value = QLabel(self.checkout_data.get('book_id', 'N/A'))
        book_id_value.setFont(QFont('Inter', 10))
        book_grid_layout.addWidget(book_id_value, 1, 2)

        # Author (if available)
        if self.checkout_data.get('book_author'):
            author_icon = QLabel("✍️")
            author_icon.setFont(QFont('Inter', 11))
            book_grid_layout.addWidget(author_icon, 2, 0)

            author_label = QLabel("Author:")
            author_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
            author_label.setStyleSheet('color: #666;')
            book_grid_layout.addWidget(author_label, 2, 1)

            author_value = QLabel(self.checkout_data['book_author'])
            author_value.setFont(QFont('Inter', 10))
            book_grid_layout.addWidget(author_value, 2, 2)

        book_grid_layout.setColumnStretch(2, 1)
        info_layout.addWidget(book_grid)

        # Divider
        divider3 = QFrame()
        divider3.setFrameShape(QFrame.Shape.HLine)
        divider3.setStyleSheet("background-color: #E0E0E0; max-height: 1px; margin: 5px 0;")
        info_layout.addWidget(divider3)

        # Return Information Section (within card)
        return_header = QLabel("📅 RETURN INFORMATION")
        return_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        return_header.setStyleSheet('color: #FF9800; padding-bottom: 5px;')
        info_layout.addWidget(return_header)

        # Return details grid
        return_grid = QWidget()
        return_grid_layout = QGridLayout(return_grid)
        return_grid_layout.setContentsMargins(10, 0, 0, 0)
        return_grid_layout.setVerticalSpacing(8)
        return_grid_layout.setHorizontalSpacing(15)

        # Checkout date
        checkout_icon = QLabel("📤")
        checkout_icon.setFont(QFont('Inter', 11))
        return_grid_layout.addWidget(checkout_icon, 0, 0)

        checkout_label = QLabel("Checked Out:")
        checkout_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        checkout_label.setStyleSheet('color: #666;')
        return_grid_layout.addWidget(checkout_label, 0, 1)

        checkout_value = QLabel(self.checkout_data.get('checkout_date', 'N/A'))
        checkout_value.setFont(QFont('Inter', 10))
        return_grid_layout.addWidget(checkout_value, 0, 2)

        # Due date
        due_icon = QLabel("⚠️")
        due_icon.setFont(QFont('Inter', 11))
        return_grid_layout.addWidget(due_icon, 1, 0)

        due_label = QLabel("Due Date:")
        due_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        due_label.setStyleSheet('color: #666;')
        return_grid_layout.addWidget(due_label, 1, 1)

        due_value = QLabel(self.checkout_data.get('due_date', 'N/A'))
        due_value.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        due_value.setStyleSheet('color: #F44336;')
        return_grid_layout.addWidget(due_value, 1, 2)

        return_grid_layout.setColumnStretch(2, 1)
        info_layout.addWidget(return_grid)

        # Late fee warning (now inside the card)
        fee_warning = QLabel("* A late fee of 50 per day will be charged for overdue returns")
        fee_warning.setFont(QFont('Inter', 9))
        fee_warning.setStyleSheet('color: #999; margin-top: 5px;')
        fee_warning.setWordWrap(True)
        info_layout.addWidget(fee_warning)

        receipt_layout.addWidget(info_card)

        # Additional notes
        notes_widget = QWidget()
        notes_layout = QVBoxLayout(notes_widget)
        notes_layout.setContentsMargins(10, 10, 10, 10)

        thanks_label = QLabel("Thank you for using Wise Owl Library!")
        thanks_label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        thanks_label.setStyleSheet('color: #4CAF50;')
        thanks_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        notes_layout.addWidget(thanks_label)

        receipt_layout.addWidget(notes_widget)

        # Footer
        footer = QFrame()
        footer.setFrameShape(QFrame.Shape.HLine)
        footer.setFrameShadow(QFrame.Shadow.Sunken)
        footer.setStyleSheet("background-color: #E0E0E0; max-height: 1px; margin-top: 10px;")
        receipt_layout.addWidget(footer)

        footer_text = QLabel("This is your official checkout receipt. Please keep it for your records.")
        footer_text.setFont(QFont('Inter', 9))
        footer_text.setStyleSheet('color: #999;')
        footer_text.setWordWrap(True)
        footer_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        receipt_layout.addWidget(footer_text)

        receipt_layout.addStretch()

        # Set the container as the scroll area widget
        scroll.setWidget(self.container)
        layout.addWidget(scroll)

        # Button section (fixed at bottom)
        button_widget = QWidget()
        button_widget.setStyleSheet('''
            QWidget {
                background-color: white;
                border-top: 1px solid #E0E0E0;
                padding: 15px;
            }
        ''')
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(20, 10, 20, 10)

        # PDF Export button
        self.pdf_btn = QPushButton("📄 Export to PDF")
        self.pdf_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.pdf_btn.setFixedHeight(40)
        self.pdf_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
        ''')
        self.pdf_btn.clicked.connect(self.export_to_pdf)
        button_layout.addWidget(self.pdf_btn)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet('''
            QPushButton {
                background-color: #F5F5F5;
                color: #333;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        ''')
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addWidget(button_widget)

    def export_to_pdf(self):
        """Export the receipt to a PDF file with proper formatting and multi-page support"""
        from PyQt6.QtPrintSupport import QPrinter
        from PyQt6.QtGui import QPainter, QPageSize, QPageLayout
        from PyQt6.QtCore import QMarginsF, QDate

        # Ask user where to save the PDF
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Receipt as PDF",
            f"checkout_receipt_{QDate.currentDate().toString('yyyy-MM-dd')}.pdf",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)

            # Set to portrait A4
            printer.setPageOrientation(QPageLayout.Orientation.Portrait)
            page_size = QPageSize(QPageSize.PageSizeId.A4)
            printer.setPageSize(page_size)

            # Use minimal margins
            margins = QMarginsF(10, 10, 10, 10)
            printer.setPageMargins(margins, QPageLayout.Unit.Millimeter)

            painter = QPainter()
            painter.begin(printer)

            if self.container:

                page_rect = printer.pageLayout().paintRectPixels(printer.resolution())
                container_size = self.container.size()
                scale_x = page_rect.width() / container_size.width()
                scale = scale_x
                scaled_height = container_size.height() * scale
                page_height = page_rect.height()
                total_pages = max(1, int(scaled_height / page_height) + 1)

                # Render each page
                for page in range(total_pages):
                    if page > 0:
                        # Start a new page
                        printer.newPage()

                    painter.save()
                    painter.scale(scale, scale)
                    y_offset = (page * page_height) / scale
                    painter.translate(0, -y_offset)

                    # Render the container
                    self.container.render(painter)
                    painter.restore()

            painter.end()

            self.show_message("Success", f"Receipt saved successfully to:\n{file_path}", "info")

        except Exception as e:
            self.show_message("Error", f"Failed to save PDF: {str(e)}", "error")

    def show_message(self, title, message, message_type="info"):
        """Show a message dialog"""
        if message_type == "info":
            QMessageBox.information(self, title, message)
        elif message_type == "warning":
            QMessageBox.warning(self, title, message)
        elif message_type == "error":
            QMessageBox.critical(self, title, message)


class CheckinReceiptDialog(QDialog):
    """Receipt-style dialog for book check-in confirmation with PDF export"""

    def __init__(self, checkin_data, parent=None):
        super().__init__(parent)
        self.checkin_data = checkin_data
        self.setWindowTitle("Check-in Receipt")
        self.setModal(True)
        self.setMinimumSize(450, 600)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)

        self.setup_ui()

    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        # Container for receipt
        self.container = QWidget()
        self.container.setStyleSheet("background-color: white;")

        receipt_layout = QVBoxLayout(self.container)
        receipt_layout.setSpacing(15)
        receipt_layout.setContentsMargins(30, 30, 30, 30)

        # Header with logo/store name
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(5)

        # Store name
        store_name = QLabel("WISE OWL LIBRARY")
        store_name.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        store_name.setStyleSheet('color: #1C0C4F;')
        store_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(store_name)

        # Receipt title
        receipt_title = QLabel("📋 CHECK-IN RECEIPT")
        receipt_title.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        receipt_title.setStyleSheet('color: #4CAF50; letter-spacing: 1px;')
        receipt_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(receipt_title)

        # Divider
        divider1 = QFrame()
        divider1.setFrameShape(QFrame.Shape.HLine)
        divider1.setFrameShadow(QFrame.Shadow.Sunken)
        divider1.setStyleSheet("background-color: #E0E0E0; max-height: 1px;")
        header_layout.addWidget(divider1)

        receipt_layout.addWidget(header_widget)

        # Date and time
        datetime_widget = QWidget()
        datetime_layout = QHBoxLayout(datetime_widget)
        datetime_layout.setContentsMargins(0, 0, 0, 0)

        current_time = QDateTime.currentDateTime()
        date_str = current_time.toString("MMM dd, yyyy")
        time_str = current_time.toString("hh:mm AP")

        date_label = QLabel(f"Date: {date_str}")
        date_label.setFont(QFont('Inter', 11))
        date_label.setStyleSheet('color: #666;')

        time_label = QLabel(f"Time: {time_str}")
        time_label.setFont(QFont('Inter', 11))
        time_label.setStyleSheet('color: #666;')

        datetime_layout.addWidget(date_label)
        datetime_layout.addStretch()
        datetime_layout.addWidget(time_label)

        receipt_layout.addWidget(datetime_widget)

        # Combined information card
        info_card = QWidget()
        info_card.setStyleSheet('''
            QWidget {
                background-color: #F8F9FA;
                border-radius: 8px;
                padding: 15px;
                margin-top: 5px;
            }
        ''')
        info_layout = QVBoxLayout(info_card)
        info_layout.setSpacing(12)

        # Librarian Information (NEW)
        librarian_header = QLabel("👨‍💼 PROCESSED BY")
        librarian_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        librarian_header.setStyleSheet('color: #1C0C4F; padding-bottom: 5px;')
        info_layout.addWidget(librarian_header)

        librarian_grid = QWidget()
        librarian_grid_layout = QGridLayout(librarian_grid)
        librarian_grid_layout.setContentsMargins(10, 0, 0, 0)
        librarian_grid_layout.setVerticalSpacing(8)
        librarian_grid_layout.setHorizontalSpacing(15)

        # Librarian Name
        librarian_icon = QLabel("👤")
        librarian_icon.setFont(QFont('Inter', 11))
        librarian_grid_layout.addWidget(librarian_icon, 0, 0)

        librarian_label = QLabel("Librarian:")
        librarian_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        librarian_label.setStyleSheet('color: #666;')
        librarian_grid_layout.addWidget(librarian_label, 0, 1)

        librarian_value = QLabel(self.checkin_data.get('librarian_name', 'N/A'))
        librarian_value.setFont(QFont('Inter', 10))
        librarian_grid_layout.addWidget(librarian_value, 0, 2)

        # Librarian ID
        librarian_id_icon = QLabel("🆔")
        librarian_id_icon.setFont(QFont('Inter', 11))
        librarian_grid_layout.addWidget(librarian_id_icon, 1, 0)

        librarian_id_label = QLabel("Staff ID:")
        librarian_id_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        librarian_id_label.setStyleSheet('color: #666;')
        librarian_grid_layout.addWidget(librarian_id_label, 1, 1)

        librarian_id_value = QLabel(self.checkin_data.get('librarian_id', 'N/A'))
        librarian_id_value.setFont(QFont('Inter', 10))
        librarian_grid_layout.addWidget(librarian_id_value, 1, 2)

        librarian_grid_layout.setColumnStretch(2, 1)
        info_layout.addWidget(librarian_grid)

        # Divider
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.Shape.HLine)
        divider2.setStyleSheet("background-color: #E0E0E0; max-height: 1px; margin: 5px 0;")
        info_layout.addWidget(divider2)

        # Member Information Section
        member_header = QLabel("👤 MEMBER INFORMATION")
        member_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        member_header.setStyleSheet('color: #1C0C4F; padding-bottom: 5px;')
        info_layout.addWidget(member_header)

        member_grid = QWidget()
        member_grid_layout = QGridLayout(member_grid)
        member_grid_layout.setContentsMargins(10, 0, 0, 0)
        member_grid_layout.setVerticalSpacing(8)
        member_grid_layout.setHorizontalSpacing(15)

        # Member Name
        name_icon = QLabel("👤")
        name_icon.setFont(QFont('Inter', 11))
        member_grid_layout.addWidget(name_icon, 0, 0)

        name_label = QLabel("Name:")
        name_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        name_label.setStyleSheet('color: #666;')
        member_grid_layout.addWidget(name_label, 0, 1)

        name_value = QLabel(self.checkin_data.get('member_name', 'N/A'))
        name_value.setFont(QFont('Inter', 10))
        member_grid_layout.addWidget(name_value, 0, 2)

        # Member ID
        id_icon = QLabel("🆔")
        id_icon.setFont(QFont('Inter', 11))
        member_grid_layout.addWidget(id_icon, 1, 0)

        id_label = QLabel("Member ID:")
        id_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        id_label.setStyleSheet('color: #666;')
        member_grid_layout.addWidget(id_label, 1, 1)

        id_value = QLabel(self.checkin_data.get('member_id', 'N/A'))
        id_value.setFont(QFont('Inter', 10))
        member_grid_layout.addWidget(id_value, 1, 2)

        member_grid_layout.setColumnStretch(2, 1)
        info_layout.addWidget(member_grid)

        # Divider
        divider3 = QFrame()
        divider3.setFrameShape(QFrame.Shape.HLine)
        divider3.setStyleSheet("background-color: #E0E0E0; max-height: 1px; margin: 5px 0;")
        info_layout.addWidget(divider3)

        # Book Information Section
        book_header = QLabel("📚 BOOK INFORMATION")
        book_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        book_header.setStyleSheet('color: #336DED; padding-bottom: 5px;')
        info_layout.addWidget(book_header)

        book_grid = QWidget()
        book_grid_layout = QGridLayout(book_grid)
        book_grid_layout.setContentsMargins(10, 0, 0, 0)
        book_grid_layout.setVerticalSpacing(8)
        book_grid_layout.setHorizontalSpacing(15)

        # Book Title
        title_icon = QLabel("📖")
        title_icon.setFont(QFont('Inter', 11))
        book_grid_layout.addWidget(title_icon, 0, 0)

        title_label = QLabel("Title:")
        title_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        title_label.setStyleSheet('color: #666;')
        book_grid_layout.addWidget(title_label, 0, 1)

        title_value = QLabel(self.checkin_data.get('book_title', 'N/A'))
        title_value.setFont(QFont('Inter', 10))
        title_value.setWordWrap(True)
        book_grid_layout.addWidget(title_value, 0, 2)

        # Book ID
        book_id_icon = QLabel("🔖")
        book_id_icon.setFont(QFont('Inter', 11))
        book_grid_layout.addWidget(book_id_icon, 1, 0)

        book_id_label = QLabel("Book ID:")
        book_id_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        book_id_label.setStyleSheet('color: #666;')
        book_grid_layout.addWidget(book_id_label, 1, 1)

        book_id_value = QLabel(self.checkin_data.get('book_id', 'N/A'))
        book_id_value.setFont(QFont('Inter', 10))
        book_grid_layout.addWidget(book_id_value, 1, 2)

        # Author
        author_icon = QLabel("✍️")
        author_icon.setFont(QFont('Inter', 11))
        book_grid_layout.addWidget(author_icon, 2, 0)

        author_label = QLabel("Author:")
        author_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        author_label.setStyleSheet('color: #666;')
        book_grid_layout.addWidget(author_label, 2, 1)

        author_value = QLabel(self.checkin_data.get('book_author', 'N/A'))
        author_value.setFont(QFont('Inter', 10))
        book_grid_layout.addWidget(author_value, 2, 2)

        book_grid_layout.setColumnStretch(2, 1)
        info_layout.addWidget(book_grid)

        # Condition Information
        condition_header = QLabel("📊 BOOK CONDITION")
        condition_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        condition_header.setStyleSheet('color: #FF9800; padding-bottom: 5px;')
        info_layout.addWidget(condition_header)

        condition_grid = QWidget()
        condition_grid_layout = QGridLayout(condition_grid)
        condition_grid_layout.setContentsMargins(10, 0, 0, 0)
        condition_grid_layout.setVerticalSpacing(8)
        condition_grid_layout.setHorizontalSpacing(15)

        # Condition
        condition_icon = QLabel("🔍")
        condition_icon.setFont(QFont('Inter', 11))
        condition_grid_layout.addWidget(condition_icon, 0, 0)

        condition_label = QLabel("Condition:")
        condition_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        condition_label.setStyleSheet('color: #666;')
        condition_grid_layout.addWidget(condition_label, 0, 1)

        condition_value = QLabel(self.checkin_data.get('condition', 'N/A'))
        condition_value.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        condition_color = "#4CAF50" if self.checkin_data.get('condition') == "Good" else "#FF9800"
        condition_value.setStyleSheet(
            f'color: white; background-color: {condition_color}; padding: 2px 10px; border-radius: 4px;')
        condition_grid_layout.addWidget(condition_value, 0, 2)

        condition_grid_layout.setColumnStretch(2, 1)
        info_layout.addWidget(condition_grid)

        # Return Information
        return_header = QLabel("📅 RETURN INFORMATION")
        return_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        return_header.setStyleSheet('color: #336DED; padding-bottom: 5px;')
        info_layout.addWidget(return_header)

        return_grid = QWidget()
        return_grid_layout = QGridLayout(return_grid)
        return_grid_layout.setContentsMargins(10, 0, 0, 0)
        return_grid_layout.setVerticalSpacing(8)
        return_grid_layout.setHorizontalSpacing(15)

        # Borrow Date
        borrow_icon = QLabel("📅")
        borrow_icon.setFont(QFont('Inter', 11))
        return_grid_layout.addWidget(borrow_icon, 0, 0)

        borrow_label = QLabel("Borrowed:")
        borrow_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        borrow_label.setStyleSheet('color: #666;')
        return_grid_layout.addWidget(borrow_label, 0, 1)

        borrow_value = QLabel(self.checkin_data.get('borrow_date', 'N/A'))
        borrow_value.setFont(QFont('Inter', 10))
        return_grid_layout.addWidget(borrow_value, 0, 2)

        # Due Date
        due_icon = QLabel("⚠️")
        due_icon.setFont(QFont('Inter', 11))
        return_grid_layout.addWidget(due_icon, 1, 0)

        due_label = QLabel("Due Date:")
        due_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        due_label.setStyleSheet('color: #666;')
        return_grid_layout.addWidget(due_label, 1, 1)

        due_value = QLabel(self.checkin_data.get('due_date', 'N/A'))
        due_value.setFont(QFont('Inter', 10))
        return_grid_layout.addWidget(due_value, 1, 2)

        # Return Date
        return_icon = QLabel("📥")
        return_icon.setFont(QFont('Inter', 11))
        return_grid_layout.addWidget(return_icon, 2, 0)

        return_label = QLabel("Returned:")
        return_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        return_label.setStyleSheet('color: #666;')
        return_grid_layout.addWidget(return_label, 2, 1)

        return_value = QLabel(self.checkin_data.get('return_date', 'N/A'))
        return_value.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        return_value.setStyleSheet('color: #4CAF50;')
        return_grid_layout.addWidget(return_value, 2, 2)

        return_grid_layout.setColumnStretch(2, 1)
        info_layout.addWidget(return_grid)

        receipt_layout.addWidget(info_card)

        # Additional notes
        notes_widget = QWidget()
        notes_layout = QVBoxLayout(notes_widget)
        notes_layout.setContentsMargins(10, 10, 10, 10)

        thanks_label = QLabel("Thank you for returning your book to Wise Owl Library!")
        thanks_label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
        thanks_label.setStyleSheet('color: #4CAF50;')
        thanks_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        notes_layout.addWidget(thanks_label)

        receipt_layout.addWidget(notes_widget)

        # Footer
        footer = QFrame()
        footer.setFrameShape(QFrame.Shape.HLine)
        footer.setFrameShadow(QFrame.Shadow.Sunken)
        footer.setStyleSheet("background-color: #E0E0E0; max-height: 1px; margin-top: 10px;")
        receipt_layout.addWidget(footer)

        footer_text = QLabel("This is your official check-in receipt. Please keep it for your records.")
        footer_text.setFont(QFont('Inter', 9))
        footer_text.setStyleSheet('color: #999;')
        footer_text.setWordWrap(True)
        footer_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        receipt_layout.addWidget(footer_text)

        receipt_layout.addStretch()

        # Set the container as the scroll area widget
        scroll.setWidget(self.container)
        layout.addWidget(scroll)

        # Button section (fixed at bottom)
        button_widget = QWidget()
        button_widget.setStyleSheet('''
            QWidget {
                background-color: white;
                border-top: 1px solid #E0E0E0;
                padding: 15px;
            }
        ''')
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(20, 10, 20, 10)

        # PDF Export button
        self.pdf_btn = QPushButton("📄 Export to PDF")
        self.pdf_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.pdf_btn.setFixedHeight(40)
        self.pdf_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
        ''')
        self.pdf_btn.clicked.connect(self.export_to_pdf)
        button_layout.addWidget(self.pdf_btn)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet('''
            QPushButton {
                background-color: #F5F5F5;
                color: #333;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        ''')
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addWidget(button_widget)

    def export_to_pdf(self):
        """Export the receipt to a PDF file with proper formatting and multi-page support"""
        from PyQt6.QtPrintSupport import QPrinter
        from PyQt6.QtGui import QPainter, QPageSize, QPageLayout
        from PyQt6.QtCore import QMarginsF, QDate

        # Ask user where to save the PDF
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Receipt as PDF",
            f"checkin_receipt_{QDate.currentDate().toString('yyyy-MM-dd')}.pdf",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)

            # Set to portrait A4
            printer.setPageOrientation(QPageLayout.Orientation.Portrait)
            page_size = QPageSize(QPageSize.PageSizeId.A4)
            printer.setPageSize(page_size)

            # Use minimal margins
            margins = QMarginsF(10, 10, 10, 10)
            printer.setPageMargins(margins, QPageLayout.Unit.Millimeter)

            painter = QPainter()
            painter.begin(printer)

            if self.container:

                page_rect = printer.pageLayout().paintRectPixels(printer.resolution())
                container_size = self.container.size()
                scale_x = page_rect.width() / container_size.width()
                scale = scale_x
                scaled_height = container_size.height() * scale
                page_height = page_rect.height()
                total_pages = max(1, int(scaled_height / page_height) + 1)

                # Render each page
                for page in range(total_pages):
                    if page > 0:
                        printer.newPage()

                    painter.save()
                    painter.scale(scale, scale)

                    y_offset = (page * page_height) / scale
                    painter.translate(0, -y_offset)

                    self.container.render(painter)
                    painter.restore()

            painter.end()

            self.show_message("Success", f"Receipt saved successfully to:\n{file_path}", "info")

        except Exception as e:
            self.show_message("Error", f"Failed to save PDF: {str(e)}", "error")

    def show_message(self, title, message, message_type="info"):
        """Show a message dialog"""
        if message_type == "info":
            QMessageBox.information(self, title, message)
        elif message_type == "warning":
            QMessageBox.warning(self, title, message)
        elif message_type == "error":
            QMessageBox.critical(self, title, message)


class CheckinDueDialog(QDialog):
    """Dialog for check-in with overdue fee calculation"""

    def __init__(self, checkin_data, parent=None):
        super().__init__(parent)
        self.checkin_data = checkin_data
        self.days_overdue = checkin_data.get('days_overdue', 0)
        self.fee_per_day = 50  # 50 per day fee
        self.total_fee = self.days_overdue * self.fee_per_day

        self.setWindowTitle("⚠️ Overdue Book Check-in")
        self.setModal(True)
        self.setMinimumSize(500, 600)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)

        self.setup_ui()

    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        # Container for receipt - NO CARD STYLING
        self.container = QWidget()
        self.container.setStyleSheet("background-color: white;")

        receipt_layout = QVBoxLayout(self.container)
        receipt_layout.setSpacing(15)
        receipt_layout.setContentsMargins(30, 30, 30, 30)

        # Header with warning
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(5)

        # Store name
        store_name = QLabel("WISE OWL LIBRARY")
        store_name.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        store_name.setStyleSheet('color: #1C0C4F;')
        store_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(store_name)

        # Warning icon and title
        warning_widget = QWidget()
        warning_layout = QHBoxLayout(warning_widget)
        warning_layout.setContentsMargins(0, 5, 0, 5)
        warning_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        warning_icon = QLabel("⚠️")
        warning_icon.setFont(QFont('Inter', 28))
        warning_icon.setStyleSheet('color: #F44336;')
        warning_layout.addWidget(warning_icon)

        receipt_title = QLabel("OVERDUE BOOK RETURN")
        receipt_title.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        receipt_title.setStyleSheet('color: #F44336; letter-spacing: 1px;')
        warning_layout.addWidget(receipt_title)

        header_layout.addWidget(warning_widget)

        # Divider
        divider1 = QFrame()
        divider1.setFrameShape(QFrame.Shape.HLine)
        divider1.setFrameShadow(QFrame.Shadow.Sunken)
        divider1.setStyleSheet("background-color: #F44336; max-height: 2px;")
        header_layout.addWidget(divider1)

        receipt_layout.addWidget(header_widget)

        # Date and time
        datetime_widget = QWidget()
        datetime_layout = QHBoxLayout(datetime_widget)
        datetime_layout.setContentsMargins(0, 0, 0, 0)

        current_time = QDateTime.currentDateTime()
        date_str = current_time.toString("MMM dd, yyyy")
        time_str = current_time.toString("hh:mm AP")

        date_label = QLabel(f"Date: {date_str}")
        date_label.setFont(QFont('Inter', 11))
        date_label.setStyleSheet('color: #666;')

        time_label = QLabel(f"Time: {time_str}")
        time_label.setFont(QFont('Inter', 11))
        time_label.setStyleSheet('color: #666;')

        datetime_layout.addWidget(date_label)
        datetime_layout.addStretch()
        datetime_layout.addWidget(time_label)

        receipt_layout.addWidget(datetime_widget)

        # Librarian Information - NO CARD
        librarian_header = QLabel("👨‍💼 PROCESSED BY")
        librarian_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        librarian_header.setStyleSheet('color: #1C0C4F; padding-bottom: 5px;')
        receipt_layout.addWidget(librarian_header)

        librarian_grid = QWidget()
        librarian_grid_layout = QGridLayout(librarian_grid)
        librarian_grid_layout.setContentsMargins(10, 0, 0, 0)
        librarian_grid_layout.setVerticalSpacing(8)
        librarian_grid_layout.setHorizontalSpacing(15)

        # Librarian Name
        librarian_icon = QLabel("👤")
        librarian_icon.setFont(QFont('Inter', 11))
        librarian_grid_layout.addWidget(librarian_icon, 0, 0)

        librarian_label = QLabel("Librarian:")
        librarian_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        librarian_label.setStyleSheet('color: #666;')
        librarian_grid_layout.addWidget(librarian_label, 0, 1)

        librarian_value = QLabel(self.checkin_data.get('librarian_name', 'N/A'))
        librarian_value.setFont(QFont('Inter', 10))
        librarian_grid_layout.addWidget(librarian_value, 0, 2)

        # Librarian ID
        librarian_id_icon = QLabel("🆔")
        librarian_id_icon.setFont(QFont('Inter', 11))
        librarian_grid_layout.addWidget(librarian_id_icon, 1, 0)

        librarian_id_label = QLabel("Staff ID:")
        librarian_id_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        librarian_id_label.setStyleSheet('color: #666;')
        librarian_grid_layout.addWidget(librarian_id_label, 1, 1)

        librarian_id_value = QLabel(self.checkin_data.get('librarian_id', 'N/A'))
        librarian_id_value.setFont(QFont('Inter', 10))
        librarian_grid_layout.addWidget(librarian_id_value, 1, 2)

        librarian_grid_layout.setColumnStretch(2, 1)
        receipt_layout.addWidget(librarian_grid)

        # Divider
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.Shape.HLine)
        divider2.setStyleSheet("background-color: #E0E0E0; max-height: 1px; margin: 5px 0;")
        receipt_layout.addWidget(divider2)

        # Member Information - NO CARD
        member_header = QLabel("👤 MEMBER INFORMATION")
        member_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        member_header.setStyleSheet('color: #1C0C4F; padding-bottom: 5px;')
        receipt_layout.addWidget(member_header)

        member_grid = QWidget()
        member_grid_layout = QGridLayout(member_grid)
        member_grid_layout.setContentsMargins(10, 0, 0, 0)
        member_grid_layout.setVerticalSpacing(8)
        member_grid_layout.setHorizontalSpacing(15)

        # Member Name
        name_icon = QLabel("👤")
        name_icon.setFont(QFont('Inter', 11))
        member_grid_layout.addWidget(name_icon, 0, 0)

        name_label = QLabel("Name:")
        name_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        name_label.setStyleSheet('color: #666;')
        member_grid_layout.addWidget(name_label, 0, 1)

        name_value = QLabel(self.checkin_data.get('member_name', 'N/A'))
        name_value.setFont(QFont('Inter', 10))
        member_grid_layout.addWidget(name_value, 0, 2)

        # Member ID
        id_icon = QLabel("🆔")
        id_icon.setFont(QFont('Inter', 11))
        member_grid_layout.addWidget(id_icon, 1, 0)

        id_label = QLabel("Member ID:")
        id_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        id_label.setStyleSheet('color: #666;')
        member_grid_layout.addWidget(id_label, 1, 1)

        id_value = QLabel(self.checkin_data.get('member_id', 'N/A'))
        id_value.setFont(QFont('Inter', 10))
        member_grid_layout.addWidget(id_value, 1, 2)

        member_grid_layout.setColumnStretch(2, 1)
        receipt_layout.addWidget(member_grid)

        # Divider
        divider3 = QFrame()
        divider3.setFrameShape(QFrame.Shape.HLine)
        divider3.setStyleSheet("background-color: #E0E0E0; max-height: 1px; margin: 5px 0;")
        receipt_layout.addWidget(divider3)

        # Book Information - NO CARD
        book_header = QLabel("📚 BOOK INFORMATION")
        book_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        book_header.setStyleSheet('color: #336DED; padding-bottom: 5px;')
        receipt_layout.addWidget(book_header)

        book_grid = QWidget()
        book_grid_layout = QGridLayout(book_grid)
        book_grid_layout.setContentsMargins(10, 0, 0, 0)
        book_grid_layout.setVerticalSpacing(8)
        book_grid_layout.setHorizontalSpacing(15)

        # Book Title
        title_icon = QLabel("📖")
        title_icon.setFont(QFont('Inter', 11))
        book_grid_layout.addWidget(title_icon, 0, 0)

        title_label = QLabel("Title:")
        title_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        title_label.setStyleSheet('color: #666;')
        book_grid_layout.addWidget(title_label, 0, 1)

        title_value = QLabel(self.checkin_data.get('book_title', 'N/A'))
        title_value.setFont(QFont('Inter', 10))
        title_value.setWordWrap(True)
        book_grid_layout.addWidget(title_value, 0, 2)

        # Book ID
        book_id_icon = QLabel("🔖")
        book_id_icon.setFont(QFont('Inter', 11))
        book_grid_layout.addWidget(book_id_icon, 1, 0)

        book_id_label = QLabel("Book ID:")
        book_id_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        book_id_label.setStyleSheet('color: #666;')
        book_grid_layout.addWidget(book_id_label, 1, 1)

        book_id_value = QLabel(self.checkin_data.get('book_id', 'N/A'))
        book_id_value.setFont(QFont('Inter', 10))
        book_grid_layout.addWidget(book_id_value, 1, 2)

        # Author
        author_icon = QLabel("✍️")
        author_icon.setFont(QFont('Inter', 11))
        book_grid_layout.addWidget(author_icon, 2, 0)

        author_label = QLabel("Author:")
        author_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        author_label.setStyleSheet('color: #666;')
        book_grid_layout.addWidget(author_label, 2, 1)

        author_value = QLabel(self.checkin_data.get('book_author', 'N/A'))
        author_value.setFont(QFont('Inter', 10))
        book_grid_layout.addWidget(author_value, 2, 2)

        book_grid_layout.setColumnStretch(2, 1)
        receipt_layout.addWidget(book_grid)

        # Divider
        divider4 = QFrame()
        divider4.setFrameShape(QFrame.Shape.HLine)
        divider4.setStyleSheet("background-color: #E0E0E0; max-height: 1px; margin: 5px 0;")
        receipt_layout.addWidget(divider4)

        # Condition Information - NO CARD
        condition_header = QLabel("📊 BOOK CONDITION")
        condition_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        condition_header.setStyleSheet('color: #FF9800; padding-bottom: 5px;')
        receipt_layout.addWidget(condition_header)

        condition_grid = QWidget()
        condition_grid_layout = QGridLayout(condition_grid)
        condition_grid_layout.setContentsMargins(10, 0, 0, 0)
        condition_grid_layout.setVerticalSpacing(8)
        condition_grid_layout.setHorizontalSpacing(15)

        # Condition
        condition_icon = QLabel("🔍")
        condition_icon.setFont(QFont('Inter', 11))
        condition_grid_layout.addWidget(condition_icon, 0, 0)

        condition_label = QLabel("Condition:")
        condition_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        condition_label.setStyleSheet('color: #666;')
        condition_grid_layout.addWidget(condition_label, 0, 1)

        condition_value = QLabel(self.checkin_data.get('condition', 'N/A'))
        condition_value.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        condition_color = "#4CAF50" if self.checkin_data.get('condition') == "Good" else "#FF9800"
        condition_value.setStyleSheet(
            f'color: white; background-color: {condition_color}; padding: 2px 10px; border-radius: 4px;')
        condition_grid_layout.addWidget(condition_value, 0, 2)

        condition_grid_layout.setColumnStretch(2, 1)
        receipt_layout.addWidget(condition_grid)

        # Divider
        divider5 = QFrame()
        divider5.setFrameShape(QFrame.Shape.HLine)
        divider5.setStyleSheet("background-color: #E0E0E0; max-height: 1px; margin: 5px 0;")
        receipt_layout.addWidget(divider5)

        # Return Information - NO CARD
        return_header = QLabel("📅 RETURN INFORMATION")
        return_header.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        return_header.setStyleSheet('color: #336DED; padding-bottom: 5px;')
        receipt_layout.addWidget(return_header)

        return_grid = QWidget()
        return_grid_layout = QGridLayout(return_grid)
        return_grid_layout.setContentsMargins(10, 0, 0, 0)
        return_grid_layout.setVerticalSpacing(8)
        return_grid_layout.setHorizontalSpacing(15)

        # Borrow Date
        borrow_icon = QLabel("📅")
        borrow_icon.setFont(QFont('Inter', 11))
        return_grid_layout.addWidget(borrow_icon, 0, 0)

        borrow_label = QLabel("Borrowed:")
        borrow_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        borrow_label.setStyleSheet('color: #666;')
        return_grid_layout.addWidget(borrow_label, 0, 1)

        borrow_value = QLabel(self.checkin_data.get('borrow_date', 'N/A'))
        borrow_value.setFont(QFont('Inter', 10))
        return_grid_layout.addWidget(borrow_value, 0, 2)

        # Due Date
        due_icon = QLabel("⚠️")
        due_icon.setFont(QFont('Inter', 11))
        return_grid_layout.addWidget(due_icon, 1, 0)

        due_label = QLabel("Due Date:")
        due_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        due_label.setStyleSheet('color: #666;')
        return_grid_layout.addWidget(due_label, 1, 1)

        due_value = QLabel(self.checkin_data.get('due_date', 'N/A'))
        due_value.setFont(QFont('Inter', 10))
        return_grid_layout.addWidget(due_value, 1, 2)

        # Return Date
        return_icon = QLabel("📥")
        return_icon.setFont(QFont('Inter', 11))
        return_grid_layout.addWidget(return_icon, 2, 0)

        return_label = QLabel("Returned:")
        return_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        return_label.setStyleSheet('color: #666;')
        return_grid_layout.addWidget(return_label, 2, 1)

        return_value = QLabel(self.checkin_data.get('return_date', 'N/A'))
        return_value.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        return_value.setStyleSheet('color: #4CAF50;')
        return_grid_layout.addWidget(return_value, 2, 2)

        # Days Overdue
        overdue_icon = QLabel("⏰")
        overdue_icon.setFont(QFont('Inter', 11))
        return_grid_layout.addWidget(overdue_icon, 3, 0)

        overdue_label = QLabel("Days Overdue:")
        overdue_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        overdue_label.setStyleSheet('color: #666;')
        return_grid_layout.addWidget(overdue_label, 3, 1)

        overdue_value = QLabel(f"{self.days_overdue} days")
        overdue_value.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        overdue_value.setStyleSheet('color: #F44336;')
        return_grid_layout.addWidget(overdue_value, 3, 2)

        return_grid_layout.setColumnStretch(2, 1)
        receipt_layout.addWidget(return_grid)

        # Divider
        divider6 = QFrame()
        divider6.setFrameShape(QFrame.Shape.HLine)
        divider6.setStyleSheet("background-color: #E0E0E0; max-height: 1px; margin: 5px 0;")
        receipt_layout.addWidget(divider6)

        # FEE SECTION - NO CARD, just simple text
        fee_header = QLabel("💰 OVERDUE FEE")
        fee_header.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        fee_header.setStyleSheet('color: #F44336; padding: 10px 0;')
        fee_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        receipt_layout.addWidget(fee_header)

        # Simple fee display
        total_label = QLabel(f"Total Fee: {self.total_fee}")
        total_label.setFont(QFont('Inter', 20, QFont.Weight.Bold))
        total_label.setStyleSheet('color: #F44336; padding: 5px 0;')
        total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        receipt_layout.addWidget(total_label)

        # Payment note
        payment_note = QLabel("Payment must be collected before check-in is complete.")
        payment_note.setFont(QFont('Inter', 10))
        payment_note.setStyleSheet('color: #F44336; padding: 5px 0;')
        payment_note.setWordWrap(True)
        payment_note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        receipt_layout.addWidget(payment_note)

        # Footer
        footer = QFrame()
        footer.setFrameShape(QFrame.Shape.HLine)
        footer.setFrameShadow(QFrame.Shadow.Sunken)
        footer.setStyleSheet("background-color: #F44336; max-height: 1px; margin-top: 10px;")
        receipt_layout.addWidget(footer)

        footer_text = QLabel("⚠️ This receipt includes overdue fees that must be paid.")
        footer_text.setFont(QFont('Inter', 9, QFont.Weight.Bold))
        footer_text.setStyleSheet('color: #F44336; padding: 5px 0;')
        footer_text.setWordWrap(True)
        footer_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        receipt_layout.addWidget(footer_text)

        receipt_layout.addStretch()

        # Set the container as the scroll area widget
        scroll.setWidget(self.container)
        layout.addWidget(scroll)

        # Button section (fixed at bottom)
        button_widget = QWidget()
        button_widget.setStyleSheet('''
            QWidget {
                background-color: white;
                border-top: 1px solid #E0E0E0;
                padding: 15px;
            }
        ''')
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(20, 10, 20, 10)

        # PDF Export button
        self.pdf_btn = QPushButton("📄 Export to PDF")
        self.pdf_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        self.pdf_btn.setFixedHeight(40)
        self.pdf_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
        ''')
        self.pdf_btn.clicked.connect(self.export_to_pdf)
        button_layout.addWidget(self.pdf_btn)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFont(QFont('Inter', 12, QFont.Weight.Bold))
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet('''
            QPushButton {
                background-color: #F5F5F5;
                color: #333;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        ''')
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addWidget(button_widget)

    def export_to_pdf(self):
        """Export the receipt to a PDF file with proper formatting and multi-page support"""
        from PyQt6.QtPrintSupport import QPrinter
        from PyQt6.QtGui import QPainter, QPageSize, QPageLayout
        from PyQt6.QtCore import QMarginsF, QDate

        # Ask user where to save the PDF
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Receipt as PDF",
            f"overdue_receipt_{QDate.currentDate().toString('yyyy-MM-dd')}.pdf",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)

            # Set to portrait A4
            printer.setPageOrientation(QPageLayout.Orientation.Portrait)
            page_size = QPageSize(QPageSize.PageSizeId.A4)
            printer.setPageSize(page_size)

            # Use minimal margins
            margins = QMarginsF(10, 10, 10, 10)
            printer.setPageMargins(margins, QPageLayout.Unit.Millimeter)

            painter = QPainter()
            painter.begin(printer)

            if self.container:
                page_rect = printer.pageLayout().paintRectPixels(printer.resolution())
                container_size = self.container.size()
                scale_x = page_rect.width() / container_size.width()
                scale = scale_x
                scaled_height = container_size.height() * scale
                page_height = page_rect.height()
                total_pages = max(1, int(scaled_height / page_height) + 1)

                # Render each page
                for page in range(total_pages):
                    if page > 0:
                        printer.newPage()

                    painter.save()
                    painter.scale(scale, scale)

                    y_offset = (page * page_height) / scale
                    painter.translate(0, -y_offset)

                    self.container.render(painter)
                    painter.restore()

            painter.end()

            self.show_message("Success", f"Receipt saved successfully to:\n{file_path}", "info")

        except Exception as e:
            self.show_message("Error", f"Failed to save PDF: {str(e)}", "error")

    def show_message(self, title, message, message_type="info"):
        """Show a message dialog"""
        try:
            if message_type == "info":
                QMessageBox.information(self, title, message)
            elif message_type == "warning":
                QMessageBox.warning(self, title, message)
            elif message_type == "error":
                QMessageBox.critical(self, title, message)
        except Exception as e:
            print(f"Error showing message: {e}")