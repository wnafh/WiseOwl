# View/Admin.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class AdminVerificationView(QMainWindow):
    def __init__(self, user_name, member_id, role):
        super().__init__()
        self.user_name = user_name
        self.member_id = member_id
        self.role = role

        self.controller = None
        self.verify_callback = None
        self.back_callback = None

        self.setWindowTitle("Wise Owl - Admin Verification")
        try:
            self.setWindowIcon(QIcon('View/LOGO3.png'))
        except:
            pass

        # Make window resizable
        self.setMinimumSize(400, 650)
        self.resize(500, 800)

        self.setup_ui()
        self.center()

    def setup_ui(self):
        """Pure UI setup with logo"""
        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet('background-color: white;')

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(0)
        central.setLayout(layout)

        # Logo section
        logo_widget = QWidget()
        logo_layout = QVBoxLayout(logo_widget)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.setSpacing(12)
        logo_layout.setContentsMargins(0, 0, 0, 0)

        # Load actual logo image
        logo_label = QLabel()
        try:
            pixmap = QPixmap('View/LOGO3.png')
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
            else:
                logo_label.setText("🦉")
                logo_label.setFont(QFont('Arial', 60))
        except:
            logo_label.setText("🦉")
            logo_label.setFont(QFont('Arial', 60))

        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)

        layout.addWidget(logo_widget)

        # Title
        wise = QLabel("WISE OWL")
        wise.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wise.setFont(QFont('Karma', 28, QFont.Weight.Bold))
        wise.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(wise)

        welcome = QLabel(f"Welcome, {self.user_name}!")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setFont(QFont('Inter', 14))
        welcome.setStyleSheet('color: #596975;')
        layout.addWidget(welcome)

        layout.addSpacing(25)

        # Admin Verification header
        admin_header = QLabel("Admin Verification")
        admin_header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        admin_header.setFont(QFont('Inter', 24, QFont.Weight.Bold))
        admin_header.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(admin_header)

        admin_desc = QLabel("Enter the admin access code to continue")
        admin_desc.setAlignment(Qt.AlignmentFlag.AlignLeft)
        admin_desc.setFont(QFont('Inter', 14))
        admin_desc.setStyleSheet('color: #596975;')
        layout.addWidget(admin_desc)

        layout.addSpacing(25)

        # Admin Access info - NO BOX/LINES
        access_info_widget = QWidget()
        access_info_layout = QHBoxLayout(access_info_widget)
        access_info_layout.setContentsMargins(0, 0, 0, 0)
        access_info_layout.setSpacing(15)

        # Admin icon
        admin_icon = QLabel("👨‍💼")
        admin_icon.setFont(QFont('Arial', 24))
        access_info_layout.addWidget(admin_icon)

        # Access info text - CLEAN TEXT
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(5)

        access_title = QLabel("Admin Access Required")
        access_title.setFont(QFont('Inter', 16, QFont.Weight.Bold))
        access_title.setStyleSheet('color: #1C0C4F;')
        text_layout.addWidget(access_title)

        access_desc_text = QLabel("Only authorized administrators can access this area.")
        access_desc_text.setFont(QFont('Inter', 13))
        access_desc_text.setStyleSheet('color: #596975;')
        text_layout.addWidget(access_desc_text)

        access_info_layout.addWidget(text_widget)
        layout.addWidget(access_info_widget)

        layout.addSpacing(25)

        # Admin Access Code input - CLEAN
        code_label = QLabel("Admin Access Code")
        code_label.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        code_label.setStyleSheet('color: #1C0C4F;')
        layout.addWidget(code_label)

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Enter Admin Code")
        self.code_input.setFont(QFont('Inter', 14))
        self.code_input.setFixedHeight(50)
        self.code_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.code_input.setStyleSheet('''
            QLineEdit {
                padding: 0 20px;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                background-color: #F8F9FA;
            }
            QLineEdit:focus {
                border: 2px solid #336DED;
                background-color: white;
            }
        ''')
        layout.addWidget(self.code_input)

        layout.addSpacing(25)

        # Buttons row
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setSpacing(15)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        # Back button
        back_btn = QPushButton("Back")
        back_btn.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        back_btn.setFixedHeight(55)
        back_btn.setStyleSheet('''
            QPushButton {
                background-color: white;
                color: #596975;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
                border-color: #336DED;
                color: #336DED;
            }
        ''')
        back_btn.clicked.connect(self.on_back_clicked)
        buttons_layout.addWidget(back_btn)

        # Verify button
        verify_btn = QPushButton("Verify & Login")
        verify_btn.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        verify_btn.setFixedHeight(55)
        verify_btn.setStyleSheet('''
            QPushButton {
                background-color: #1C0C4F;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2A1A6F;
            }
            QPushButton:pressed {
                background-color: #15083A;
            }
        ''')
        verify_btn.clicked.connect(self.on_verify_clicked)
        buttons_layout.addWidget(verify_btn)

        layout.addWidget(buttons_widget)
        layout.addStretch()

        # Connect Enter key
        self.code_input.returnPressed.connect(self.on_verify_clicked)

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

    # Callback methods
    def on_verify_clicked(self):
        """Collect verification data and pass to Controller"""
        access_code = self.code_input.text().strip()

        if self.verify_callback:
            self.verify_callback(access_code)

    def on_back_clicked(self):
        if self.back_callback:
            self.back_callback()

    # Methods for Controller to call
    def clear_code_input(self):
        """Clear the code input field"""
        self.code_input.clear()

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