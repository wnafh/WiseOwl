# View/Log.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class LoginView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wise Owl Login")
        try:
            self.setWindowIcon(QIcon('View/LOGO3.png'))
        except:
            pass

        # Make window resizable
        self.setMinimumSize(400, 650)
        self.resize(500, 800)

        self.login_success_callback = None
        self.login_failed_callback = None

        self.setup_ui()

        self.center()

    def setup_ui(self):
        """Pure UI setup with logo and improved spacing"""
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
        #layout.addSpacing(10)

        # Title section
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.setSpacing(8)
        title_layout.setContentsMargins(0, 0, 0, 0)

        wise = QLabel("WISE OWL")
        wise.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wise.setFont(QFont('Karma', 28, QFont.Weight.Bold))
        wise.setStyleSheet('color: #1C0C4F;')
        title_layout.addWidget(wise)

        welcome = QLabel("Welcome back! Please log in to continue")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setFont(QFont('Inter', 14))
        welcome.setStyleSheet('color: #596975;')
        title_layout.addWidget(welcome)

        layout.addWidget(title_widget)
        layout.addSpacing(35)

        # Login form section
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(0)
        form_layout.setContentsMargins(0, 0, 0, 0)

        # Log in header
        log_header = QLabel("Log in")
        log_header.setFont(QFont('Inter', 24, QFont.Weight.Bold))
        log_header.setStyleSheet('color: #1C0C4F;')
        form_layout.addWidget(log_header)

        form_layout.addSpacing(8)

        log_desc = QLabel("Enter your credentials to access the\nlibrary system.")
        log_desc.setFont(QFont('Inter', 14))
        log_desc.setStyleSheet('color: #596975;')
        form_layout.addWidget(log_desc)

        form_layout.addSpacing(30)

        # Full Name field
        name_label = QLabel("Full Name")
        name_label.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        name_label.setStyleSheet('color: #1C0C4F;')
        form_layout.addWidget(name_label)

        form_layout.addSpacing(8)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name")
        self.name_input.setFont(QFont('Inter', 14))
        self.name_input.setFixedHeight(50)
        self.name_input.setStyleSheet('''
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
        form_layout.addWidget(self.name_input)

        form_layout.addSpacing(20)

        # Member ID field
        id_label = QLabel("Member ID")
        id_label.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        id_label.setStyleSheet('color: #1C0C4F;')
        form_layout.addWidget(id_label)

        form_layout.addSpacing(8)

        self.mem_id_input = QLineEdit()
        self.mem_id_input.setPlaceholderText("Enter your member ID")
        self.mem_id_input.setFont(QFont('Inter', 14))
        self.mem_id_input.setFixedHeight(50)
        self.mem_id_input.setStyleSheet('''
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
        form_layout.addWidget(self.mem_id_input)

        form_layout.addSpacing(35)

        # Continue button
        continue_btn = QPushButton("Continue")
        continue_btn.setFont(QFont('Inter', 15, QFont.Weight.Bold))
        continue_btn.setFixedHeight(55)
        continue_btn.setStyleSheet('''
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
        continue_btn.clicked.connect(self.on_login_clicked)
        form_layout.addWidget(continue_btn)

        layout.addWidget(form_widget)
        layout.addStretch()

        # Connect Enter key
        self.name_input.returnPressed.connect(self.on_login_clicked)
        self.mem_id_input.returnPressed.connect(self.on_login_clicked)

    #centers the widget
    def center(self):
        # Get a rectangle representing the window's geometry (including frame)
        qr = self.frameGeometry()
        # Get the center point of the screen's available geometry (area not covered by taskbars, etc.)
        cp = self.screen().availableGeometry().center()
        # Move the center of the window's rectangle to the screen's center point
        qr.moveCenter(cp)
        # Move the top-left point of the application window to the top-left point of the qr rectangle
        self.move(qr.topLeft())

    def on_login_clicked(self):
        """Collect data and pass to Controller"""
        full_name = self.name_input.text().strip()
        member_id = self.mem_id_input.text().strip()

        if self.login_success_callback:
            self.login_success_callback(full_name, member_id)

    def show_error(self, message):
        """Show error dialog"""
        QMessageBox.critical(self, "Login Failed", message)

    def show_success(self, message):
        """Show success dialog"""
        QMessageBox.information(self, "Login Successful", message)

    def clear_fields(self):
        """Clear input fields"""
        self.name_input.clear()
        self.mem_id_input.clear()

    def show_message(self, title, message, message_type="info"):
        """Show a message dialog"""
        if message_type == "info":
            QMessageBox.information(self, title, message)
        elif message_type == "warning":
            QMessageBox.warning(self, title, message)
        elif message_type == "error":
            QMessageBox.critical(self, title, message)