# View/AdminDashboard.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import io


class AdminDashboardView(QMainWindow):
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
        self.checkout_callback = None
        self.checkin_callback = None

        self.setWindowTitle("Wise Owl -- Admin Dashboard")
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

        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        content = self.create_main_content()
        main_layout.addWidget(content, stretch=1)

    # Centers the widget
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

        # Header
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setSpacing(8)
        header_layout.setContentsMargins(0, 0, 0, 0)

        header = QLabel("Admin Dashboard")
        header.setFont(QFont('Karma', 28, QFont.Weight.Bold))
        header.setStyleSheet('color: #1C0C4F;')
        header_layout.addWidget(header)

        subtitle = QLabel("Manage library inventory and operations")
        subtitle.setFont(QFont('Inter', 14))
        subtitle.setStyleSheet('color: #596975;')
        header_layout.addWidget(subtitle)

        layout.addWidget(header_container)

        # Stats display - clean text without boxes
        stats_container = QWidget()
        self.stats_layout = QHBoxLayout(stats_container)
        self.stats_layout.setSpacing(40)
        self.stats_layout.setContentsMargins(0, 10, 0, 10)
        layout.addWidget(stats_container)

        # Create a horizontal layout for charts and overdue section
        charts_and_overdue_layout = QHBoxLayout()
        charts_and_overdue_layout.setSpacing(25)

        # Pie chart container
        pie_chart_container = QWidget()
        pie_chart_container.setMinimumWidth(400)
        pie_chart_container.setMaximumWidth(450)
        pie_chart_layout = QVBoxLayout(pie_chart_container)
        pie_chart_layout.setContentsMargins(0, 0, 0, 0)

        pie_chart_header = QLabel("📊 Book Status Distribution")
        pie_chart_header.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        pie_chart_header.setStyleSheet('color: #1C0C4F;')
        pie_chart_layout.addWidget(pie_chart_header)

        # Create matplotlib figure for pie chart
        self.pie_figure = Figure(figsize=(4, 4), dpi=100)
        self.pie_canvas = FigureCanvas(self.pie_figure)
        self.pie_canvas.setMinimumHeight(300)
        self.pie_canvas.setStyleSheet('background-color: transparent;')
        pie_chart_layout.addWidget(self.pie_canvas)

        charts_and_overdue_layout.addWidget(pie_chart_container)

        # Overdue books section
        overdue_section = self.create_overdue_section()
        charts_and_overdue_layout.addWidget(overdue_section, stretch=1)

        layout.addLayout(charts_and_overdue_layout)

        return widget

    def create_overdue_section(self):
        """Create overdue books section WITHOUT border box"""
        widget = QWidget()
        widget.setStyleSheet('''
            background-color: transparent;
            border: none;
        ''')

        layout = QVBoxLayout(widget)
        layout.setSpacing(18)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header with count badge
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        header_text = QLabel("⚠️  Overdue Books")
        header_text.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        header_text.setStyleSheet('color: #1C0C4F;')
        header_layout.addWidget(header_text)

        # Overdue count badge - simplified
        self.overdue_count_badge = QLabel("0")
        self.overdue_count_badge.setFont(QFont('Inter', 20, QFont.Weight.Bold))
        self.overdue_count_badge.setStyleSheet('color: #FF5252;')
        self.overdue_count_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.overdue_count_badge)

        header_layout.addStretch()
        layout.addWidget(header_widget)

        desc = QLabel("Books that need to be returned urgently")
        desc.setFont(QFont('Inter', 13))
        desc.setStyleSheet('color: #596975;')
        layout.addWidget(desc)

        # Scrollable overdue container
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet('''
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #C1C1C1;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #A8A8A8;
            }
        ''')

        self.overdue_container = QWidget()
        self.overdue_layout = QVBoxLayout(self.overdue_container)
        self.overdue_layout.setSpacing(10)
        self.overdue_layout.setContentsMargins(2, 2, 10, 2)
        self.overdue_layout.addStretch()

        scroll_area.setWidget(self.overdue_container)
        layout.addWidget(scroll_area, stretch=1)

        return widget

    def create_stat_widget(self, title, value, color, icon):
        """Create a clean text stat widget without boxes"""
        widget = QWidget()
        widget.setMinimumHeight(85)
        widget.setMaximumHeight(100)

        layout = QVBoxLayout(widget)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Value with icon
        value_widget = QWidget()
        value_layout = QHBoxLayout(value_widget)
        value_layout.setContentsMargins(0, 0, 0, 0)
        value_layout.setSpacing(8)
        value_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if icon:
            icon_label = QLabel(icon)
            icon_label.setFont(QFont('Arial', 24))
            icon_label.setStyleSheet(f'color: {color};')
            value_layout.addWidget(icon_label)

        value_label = QLabel(str(value))
        value_label.setFont(QFont('Inter', 32, QFont.Weight.Bold))
        value_label.setStyleSheet(f'color: {color};')
        value_layout.addWidget(value_label)

        layout.addWidget(value_widget)

        # Title - clean text
        title_label = QLabel(title)
        title_label.setFont(QFont('Inter', 13, QFont.Weight.Medium))
        title_label.setStyleSheet('color: #596975;')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        return widget

    def create_overdue_book_item(self, title, borrower, days):
        """Create overdue book item WITHOUT border lines"""
        widget = QWidget()
        widget.setMinimumHeight(70)
        widget.setMaximumHeight(85)

        # Urgency-based styling - NO BORDERS
        if days > 30:
            text_color = "#D32F2F"  # Red
            bg_color = "#FFEBEE"
        elif days > 14:
            text_color = "#F57C00"  # Orange
            bg_color = "#FFF3E0"
        else:
            text_color = "#FFA000"  # Yellow/Amber
            bg_color = "#FFFDE7"

        widget.setStyleSheet(f'''
            background-color: {bg_color};
            border-radius: 8px;
        ''')

        layout = QVBoxLayout(widget)
        layout.setSpacing(5)
        layout.setContentsMargins(14, 10, 14, 10)

        # Title - truncated if too long
        display_title = title
        if len(title) > 50:
            display_title = title[:47] + "..."

        title_label = QLabel(display_title)
        title_label.setFont(QFont('Inter', 12, QFont.Weight.Medium))
        title_label.setStyleSheet('color: #1C0C4F;')
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # Details in one line
        details_widget = QWidget()
        details_layout = QHBoxLayout(details_widget)
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setSpacing(15)

        # Borrower - clean text
        borrower_label = QLabel(f"👤 {borrower}")
        borrower_label.setFont(QFont('Inter', 10))
        borrower_label.setStyleSheet('color: #596975;')
        details_layout.addWidget(borrower_label)

        # Days overdue - clean text
        days_label = QLabel(f"⏰ {days} days overdue")
        days_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
        days_label.setStyleSheet(f'color: {text_color};')
        details_layout.addWidget(days_label)

        details_layout.addStretch()
        layout.addWidget(details_widget)

        return widget

    # Callback methods (same as before)
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

    # Methods for Controller to call
    def update_stats(self, stats_data):
        """Update statistics display as clean text"""
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

        for stat in stats_data:
            title = stat["title"]
            config = stat_configs.get(title, {"color": "#1C0C4F", "icon": ""})

            stat_widget = self.create_stat_widget(
                title,
                stat["value"],
                config["color"],
                config["icon"]
            )
            self.stats_layout.addWidget(stat_widget)

        # Update pie chart with the same stats data
        self.update_pie_chart(stats_data)

    def update_pie_chart(self, stats_data):
        """Create a pie chart using pandas to show book status distribution"""
        # Clear the previous figure
        self.pie_figure.clear()

        # Create a pandas DataFrame from stats data
        data = {}
        for stat in stats_data:
            if stat["title"] in ["Available", "Borrowed"]:
                data[stat["title"]] = stat["value"]

        if data:
            df = pd.DataFrame(list(data.items()), columns=['Status', 'Count'])

            # Create pie chart
            ax = self.pie_figure.add_subplot(111)
            colors = ['#4CAF50', '#FF9800']  # Green for Available, Orange for Borrowed

            wedges, texts, autotexts = ax.pie(
                df['Count'],
                labels=df['Status'],
                colors=colors,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 10, 'fontweight': 'bold'}
            )

            # Style the percentage text
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(10)
                autotext.set_fontweight('bold')

            ax.set_title('Book Status Distribution', fontsize=12, fontweight='bold', pad=20)
            self.pie_figure.tight_layout()

        # Refresh the canvas
        self.pie_canvas.draw()

    def update_overdue_books(self, overdue_books):
        """Update overdue books display with scrollable area"""
        # Clear existing items except the stretch
        while self.overdue_layout.count() > 1:  # Keep the stretch at the end
            item = self.overdue_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Update overdue count badge
        self.overdue_count_badge.setText(str(len(overdue_books)))

        if overdue_books:
            for book in overdue_books:
                book_item = self.create_overdue_book_item(
                    book["title"],
                    book["borrower"],
                    book["days"]
                )
                self.overdue_layout.insertWidget(self.overdue_layout.count() - 1, book_item)
        else:
            no_overdue_widget = QWidget()
            no_overdue_widget.setMinimumHeight(120)
            no_overdue_layout = QVBoxLayout(no_overdue_widget)
            no_overdue_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            check_icon = QLabel("✅")
            check_icon.setFont(QFont('Arial', 32))
            check_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            check_icon.setStyleSheet('color: #4CAF50;')
            no_overdue_layout.addWidget(check_icon)

            no_overdue = QLabel("All books are on time!")
            no_overdue.setFont(QFont('Inter', 14, QFont.Weight.Bold))
            no_overdue.setStyleSheet('color: #4CAF50;')
            no_overdue.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_overdue_layout.addWidget(no_overdue)

            self.overdue_layout.insertWidget(0, no_overdue_widget)

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
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, \
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes