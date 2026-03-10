# View/AdminReports.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class AdminReportsView(QMainWindow):
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
        self.generate_report_callback = None
        self.export_pdf_callback = None

        self.current_report_data = None
        self.selected_report_type = "library_overview"
        self.generated_report = False

        self.setWindowTitle("Wise Owl -- Reports & Analytics")
        try:
            self.setWindowIcon(QIcon('View/LOGO3.png'))
        except:
            pass

        self.setMinimumSize(1280, 720)
        self.resize(1440, 900)

        self.setup_ui()
        self.center()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        content_widget = QWidget()
        content_widget.setStyleSheet('background-color: #F5F5F5;')
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(25)

        reports_content = self.create_reports_content()
        content_layout.addWidget(reports_content)

        main_layout.addWidget(content_widget, stretch=1)

    # Centers the widget
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_sidebar(self):
        """Create sidebar"""
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

    def create_reports_content(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(22)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header row
        header_row = QWidget()
        header_layout = QHBoxLayout(header_row)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        header = QLabel("Reports & Analytics")
        header.setFont(QFont('Karma', 28, QFont.Weight.Bold))
        header.setStyleSheet('color: #1C0C4F;')
        header_layout.addWidget(header)

        header_layout.addStretch()

        # Export PDF button
        self.export_pdf_btn = QPushButton("📄 Export as PDF")
        self.export_pdf_btn.setFont(QFont('Inter', 13, QFont.Weight.Bold))
        self.export_pdf_btn.setFixedHeight(42)
        self.export_pdf_btn.setFixedWidth(150)
        self.export_pdf_btn.setStyleSheet('''
            QPushButton {
                background-color: #336DED;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2958C4;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
            }
        ''')
        self.export_pdf_btn.clicked.connect(self.on_export_pdf_clicked)
        self.export_pdf_btn.setEnabled(False)
        header_layout.addWidget(self.export_pdf_btn)

        layout.addWidget(header_row)

        subtitle = QLabel("Generate reports and view library analytics")
        subtitle.setFont(QFont('Inter', 14))
        subtitle.setStyleSheet('color: #596975;')
        layout.addWidget(subtitle)

        # Report type selection - ALL FOUR BUTTONS RESTORED
        report_selection_widget = QWidget()
        report_selection_layout = QVBoxLayout(report_selection_widget)
        report_selection_layout.setSpacing(14)
        report_selection_layout.setContentsMargins(0, 0, 0, 0)

        selection_label = QLabel("Select Report Type")
        selection_label.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        selection_label.setStyleSheet('color: #1C0C4F;')
        report_selection_layout.addWidget(selection_label)

        report_types_widget = QWidget()
        report_types_layout = QGridLayout(report_types_widget)
        report_types_layout.setSpacing(12)
        report_types_layout.setContentsMargins(0, 0, 0, 0)

        self.report_buttons = {}
        report_types = [
            ("📊 Library Overview", "library_overview"),
            ("📚 Books Report", "books_report"),
            ("👥 Members Report", "members_report"),
            ("🔄 Circulation Report", "circulation_report"),
        ]

        for i, (report_name, report_id) in enumerate(report_types):
            row = i // 2
            col = i % 2

            btn = QPushButton(report_name)
            btn.setFont(QFont('Inter', 13))
            btn.setMinimumHeight(70)

            if report_id == self.selected_report_type:
                btn.setStyleSheet('''
                    QPushButton {
                        background-color: #F0F5FF;
                        color: #1C0C4F;
                        border: 2px solid #336DED;
                        border-radius: 10px;
                        padding: 14px;
                        text-align: left;
                    }
                ''')
            else:
                btn.setStyleSheet('''
                    QPushButton {
                        background-color: white;
                        color: #1C0C4F;
                        border: 2px solid #E0E0E0;
                        border-radius: 10px;
                        padding: 14px;
                        text-align: left;
                    }
                    QPushButton:hover {
                        border-color: #336DED;
                        background-color: #F0F5FF;
                    }
                ''')

            btn.clicked.connect(lambda checked, rt=report_id: self.on_report_type_selected(rt))
            report_types_layout.addWidget(btn, row, col)
            self.report_buttons[report_id] = btn

        report_selection_layout.addWidget(report_types_widget)
        layout.addWidget(report_selection_widget)

        # Generate button
        self.generate_btn = QPushButton("📈 Generate Report")
        self.generate_btn.setFont(QFont('Inter', 14, QFont.Weight.Bold))
        self.generate_btn.setFixedHeight(46)
        self.generate_btn.setStyleSheet('''
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
        self.generate_btn.clicked.connect(self.on_generate_report_clicked)
        layout.addWidget(self.generate_btn)

        # Report preview section WITH SCROLLBAR
        preview_label = QLabel("Report Preview")
        preview_label.setFont(QFont('Inter', 20, QFont.Weight.Bold))
        preview_label.setStyleSheet('color: #1C0C4F; margin-top: 10px;')
        layout.addWidget(preview_label)

        # Create a scroll area with visible scrollbar
        self.report_scroll = QScrollArea()
        self.report_scroll.setWidgetResizable(True)
        self.report_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.report_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.report_scroll.setStyleSheet('''
            QScrollArea {
                border: 1px solid #E0E0E0;
                border-radius: 10px;
                background-color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0;
                width: 16px;
                border-radius: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #C0C0C0;
                min-height: 30px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical:hover {
                background: #A0A0A0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: #F0F0F0;
                height: 16px;
                border-radius: 8px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #C0C0C0;
                min-width: 30px;
                border-radius: 8px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #A0A0A0;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
                width: 0px;
            }
        ''')

        # Container for report content
        self.report_preview_container = QWidget()
        self.report_preview_container.setStyleSheet('''
            QWidget {
                background-color: white;
                padding: 20px;
            }
        ''')
        self.report_preview_layout = QVBoxLayout(self.report_preview_container)
        self.report_preview_layout.setSpacing(18)
        self.report_preview_layout.setContentsMargins(20, 20, 20, 20)

        placeholder = QLabel("Select a report type and click 'Generate Report' to view")
        placeholder.setFont(QFont('Inter', 13))
        placeholder.setStyleSheet('color: #9E9E9E; padding: 40px;')
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setMinimumHeight(300)
        self.report_preview_layout.addWidget(placeholder)

        self.report_scroll.setWidget(self.report_preview_container)
        layout.addWidget(self.report_scroll, stretch=1)

        return widget

    def create_stat_card(self, title, value, color):
        """Create stat card"""
        widget = QWidget()
        widget.setMinimumHeight(90)

        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        value_label = QLabel(str(value))
        value_label.setFont(QFont('Inter', 32, QFont.Weight.Bold))
        value_label.setStyleSheet(f'color: {color};')
        layout.addWidget(value_label)

        title_label = QLabel(title)
        title_label.setFont(QFont('Inter', 13))
        title_label.setStyleSheet('color: #596975;')
        layout.addWidget(title_label)

        return widget

    def create_report_section(self, title, data):
        """Create a report section"""
        if not data:
            return QLabel(f"No {title.lower()} data available")

        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setSpacing(12)
        section_layout.setContentsMargins(0, 0, 0, 0)

        section_title = QLabel(title)
        section_title.setFont(QFont('Inter', 18, QFont.Weight.Bold))
        section_title.setStyleSheet('color: #1C0C4F; margin-top: 10px;')
        section_layout.addWidget(section_title)

        if isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], dict):
                # Create a table for dictionary data
                headers = list(data[0].keys())

                # Header row
                header_widget = QWidget()
                header_layout = QHBoxLayout(header_widget)
                header_layout.setContentsMargins(0, 10, 0, 10)

                for header in headers:
                    header_label = QLabel(str(header).title().replace('_', ' '))
                    header_label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
                    header_label.setStyleSheet('color: #1C0C4F;')
                    header_layout.addWidget(header_label, stretch=1)

                section_layout.addWidget(header_widget)

                # Data rows
                for i, row in enumerate(data):
                    row_widget = QWidget()
                    if i % 2 == 0:
                        row_widget.setStyleSheet('background-color: #F9F9F9;')

                    row_layout = QHBoxLayout(row_widget)
                    row_layout.setContentsMargins(0, 8, 0, 8)

                    for header in headers:
                        value = str(row.get(header, ''))
                        value_label = QLabel(value)
                        value_label.setFont(QFont('Inter', 10))
                        value_label.setStyleSheet('color: #666;')
                        value_label.setWordWrap(True)
                        row_layout.addWidget(value_label, stretch=1)

                    section_layout.addWidget(row_widget)
            else:
                # Simple list display
                for item in data:
                    item_label = QLabel(f"• {item}")
                    item_label.setFont(QFont('Inter', 12))
                    item_label.setStyleSheet('color: #666;')
                    section_layout.addWidget(item_label)

        return section_widget

    # ========== CALLBACK METHODS ==========

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

    def on_report_type_selected(self, report_type):
        self.selected_report_type = report_type

        for report_id, btn in self.report_buttons.items():
            if report_id == report_type:
                btn.setStyleSheet('''
                    QPushButton {
                        background-color: #F0F5FF;
                        color: #1C0C4F;
                        border: 2px solid #336DED;
                        border-radius: 10px;
                        padding: 14px;
                        text-align: left;
                    }
                ''')
            else:
                btn.setStyleSheet('''
                    QPushButton {
                        background-color: white;
                        color: #1C0C4F;
                        border: 2px solid #E0E0E0;
                        border-radius: 10px;
                        padding: 14px;
                        text-align: left;
                    }
                    QPushButton:hover {
                        border-color: #336DED;
                        background-color: #F0F5FF;
                    }
                ''')

    def on_generate_report_clicked(self):
        if self.selected_report_type and self.generate_report_callback:
            self.generate_report_callback(self.selected_report_type)
            self.generated_report = True
        else:
            self.show_message("Select Report", "Please select a report type first", "warning")

    def on_export_pdf_clicked(self):
        """Handle export as PDF button click"""
        if not self.generated_report or not self.current_report_data:
            self.show_message("No Report", "Please generate a report first", "warning")
            return

        if self.export_pdf_callback:
            self.export_pdf_callback(self.current_report_data)
        else:
            self.export_to_pdf()

    def export_to_pdf(self):
        """Export the report to a PDF file with multiple pages if needed"""
        from PyQt6.QtPrintSupport import QPrinter
        from PyQt6.QtGui import QPainter, QPageSize, QPageLayout
        from PyQt6.QtCore import QDate, QMarginsF, QRect, QPoint

        if not self.generated_report or not self.current_report_data:
            self.show_message("No Report", "Please generate a report first", "warning")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report as PDF",
            f"Library_Report_{self.selected_report_type}_{QDate.currentDate().toString('yyyy-MM-dd')}.pdf",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)

            # Set to landscape A4
            printer.setPageOrientation(QPageLayout.Orientation.Landscape)
            page_size = QPageSize(QPageSize.PageSizeId.A4)
            printer.setPageSize(page_size)

            # Use minimal margins
            margins = QMarginsF(10, 10, 10, 10)
            printer.setPageMargins(margins, QPageLayout.Unit.Millimeter)

            painter = QPainter()
            painter.begin(printer)

            preview_container = self.report_preview_container

            if preview_container:
                # Get the page rectangle in pixels
                page_rect = printer.pageLayout().paintRectPixels(printer.resolution())

                # Get the container size
                container_size = preview_container.size()

                # Calculate scale to fill the page width
                scale_x = page_rect.width() / container_size.width()
                scale = scale_x

                # Calculate the scaled height of the container
                scaled_height = container_size.height() * scale

                # Calculate how many pages we need
                page_height = page_rect.height()
                total_pages = max(1, int(scaled_height / page_height) + 1)

                # Render each page
                for page in range(total_pages):
                    if page > 0:
                        # Start a new page
                        printer.newPage()

                    # Save painter state
                    painter.save()

                    # Apply scaling
                    painter.scale(scale, scale)

                    # Calculate y-offset for this page (which portion to render)
                    y_offset = (page * page_height) / scale

                    # Create a translated painter to render the correct portion
                    painter.translate(0, -y_offset)

                    # Render the container
                    preview_container.render(painter)

                    # Restore painter state
                    painter.restore()

            painter.end()

            self.show_message("Success", f"Report saved successfully to:\n{file_path}", "info")

        except Exception as e:
            self.show_message("Error", f"Failed to save PDF: {str(e)}", "error")

    def update_report_preview(self, report_data):
        """Update the report preview with data"""
        self.current_report_data = report_data
        self.generated_report = True
        self.export_pdf_btn.setEnabled(True)

        # Clear existing content
        while self.report_preview_layout.count():
            item = self.report_preview_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not report_data:
            placeholder = QLabel("No report data available")
            placeholder.setFont(QFont('Inter', 13))
            placeholder.setStyleSheet('color: #9E9E9E; padding: 40px;')
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setMinimumHeight(300)
            self.report_preview_layout.addWidget(placeholder)
            return

        report_type = report_data.get('report_type', 'Report')
        title_label = QLabel(f"📊 {report_type.replace('_', ' ').title()} Report")
        title_label.setFont(QFont('Inter', 22, QFont.Weight.Bold))
        title_label.setStyleSheet('color: #1C0C4F;')
        self.report_preview_layout.addWidget(title_label)

        date_label = QLabel(f"Generated on: {QDate.currentDate().toString('MMMM d, yyyy')}")
        date_label.setFont(QFont('Inter', 11))
        date_label.setStyleSheet('color: #9E9E9E;')
        self.report_preview_layout.addWidget(date_label)

        # ========== LIBRARY STATISTICS SECTION ==========
        if 'statistics' in report_data and report_data['statistics']:
            stats = report_data['statistics']

            stats_label = QLabel("📊 Library Statistics")
            stats_label.setFont(QFont('Inter', 18, QFont.Weight.Bold))
            stats_label.setStyleSheet('color: #1C0C4F; margin-top: 10px;')
            self.report_preview_layout.addWidget(stats_label)

            stats_grid = QWidget()
            stats_layout = QGridLayout(stats_grid)
            stats_layout.setSpacing(14)
            stats_layout.setContentsMargins(0, 16, 0, 16)

            # Format stats properly
            colors = ['#336DED', '#4CAF50', '#FF9800', '#F44336']
            stats_items = [
                ("Total Books", stats.get('Total Books', stats.get('total_books', '0'))),
                ("Available", stats.get('Available Books', stats.get('available_books', '0'))),
                ("Borrowed", stats.get('Borrowed Books', stats.get('borrowed_books', '0'))),
                ("Total Members", stats.get('Total Members', stats.get('total_members', '0')))
            ]

            for i, (title, value) in enumerate(stats_items):
                row = i // 2
                col = i % 2
                stat_card = self.create_stat_card(title, str(value), colors[i])
                stats_layout.addWidget(stat_card, row, col)

            self.report_preview_layout.addWidget(stats_grid)

        # ========== OVERDUE BOOKS SECTION ==========
        if 'overdue_books' in report_data and report_data['overdue_books']:
            overdue_books = report_data['overdue_books']

            overdue_header = QLabel("⚠️ Overdue Books")
            overdue_header.setFont(QFont('Inter', 18, QFont.Weight.Bold))
            overdue_header.setStyleSheet('color: #F44336; margin-top: 20px;')
            self.report_preview_layout.addWidget(overdue_header)

            # Create overdue books table
            overdue_container = QWidget()
            overdue_layout = QVBoxLayout(overdue_container)
            overdue_layout.setSpacing(8)

            # Headers
            header_widget = QWidget()
            header_layout = QHBoxLayout(header_widget)
            header_layout.setContentsMargins(0, 10, 0, 10)
            header_layout.setSpacing(10)

            headers = ['Book Title', 'Borrower', 'Days Overdue', 'Fee']
            widths = [300, 200, 100, 100]

            for header, width in zip(headers, widths):
                label = QLabel(header)
                label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
                label.setStyleSheet('color: #1C0C4F;')
                label.setFixedWidth(width)
                header_layout.addWidget(label)

            header_layout.addStretch()
            overdue_layout.addWidget(header_widget)

            # Overdue book rows
            for i, book in enumerate(overdue_books):
                row_widget = QWidget()
                if i % 2 == 0:
                    row_widget.setStyleSheet('background-color: #FFF3F3;')

                row_layout = QHBoxLayout(row_widget)
                row_layout.setContentsMargins(0, 8, 0, 8)
                row_layout.setSpacing(10)

                # Title
                title_label = QLabel(book.get('title', 'N/A'))
                title_label.setFont(QFont('Inter', 10))
                title_label.setFixedWidth(300)
                title_label.setWordWrap(True)
                row_layout.addWidget(title_label)

                # Borrower
                borrower_label = QLabel(book.get('borrower', 'N/A'))
                borrower_label.setFont(QFont('Inter', 10))
                borrower_label.setFixedWidth(200)
                row_layout.addWidget(borrower_label)

                # Days
                days = str(book.get('days', book.get('days_overdue', 0)))
                days_label = QLabel(f"{days} days")
                days_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
                days_label.setFixedWidth(100)
                days_label.setStyleSheet('color: #F44336;')
                row_layout.addWidget(days_label)

                # Fee
                fee = int(days) * 50 if days.isdigit() else 0
                fee_label = QLabel(f"₱{fee}")
                fee_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
                fee_label.setFixedWidth(100)
                fee_label.setStyleSheet('color: #F44336;')
                fee_label.setAlignment(Qt.AlignmentFlag.AlignRight)
                row_layout.addWidget(fee_label)

                row_layout.addStretch()
                overdue_layout.addWidget(row_widget)

            self.report_preview_layout.addWidget(overdue_container)

        # ========== TRANSACTIONS SECTION ==========
        if 'transactions' in report_data and report_data['transactions']:
            transactions = report_data['transactions']

            trans_header = QLabel("📋 Recent Transactions")
            trans_header.setFont(QFont('Inter', 18, QFont.Weight.Bold))
            trans_header.setStyleSheet('color: #1C0C4F; margin-top: 20px;')
            self.report_preview_layout.addWidget(trans_header)

            # Create transaction table
            trans_container = QWidget()
            trans_layout = QVBoxLayout(trans_container)
            trans_layout.setSpacing(8)

            # Table headers - with proper column widths
            header_widget = QWidget()
            header_layout = QHBoxLayout(header_widget)
            header_layout.setContentsMargins(0, 10, 0, 10)
            header_layout.setSpacing(10)

            headers = ['Date', 'Member', 'Book', 'Librarian', 'Status']
            header_widths = [120, 180, 280, 180, 100]

            for header, width in zip(headers, header_widths):
                label = QLabel(header)
                label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
                label.setStyleSheet('color: #1C0C4F;')
                label.setFixedWidth(width)
                header_layout.addWidget(label)

            header_layout.addStretch()
            trans_layout.addWidget(header_widget)

            # Transaction rows
            for i, trans in enumerate(transactions[:20]):
                row_widget = QWidget()
                if i % 2 == 0:
                    row_widget.setStyleSheet('background-color: #F9F9F9;')

                row_layout = QHBoxLayout(row_widget)
                row_layout.setContentsMargins(0, 8, 0, 8)
                row_layout.setSpacing(10)

                # Date - FIXED to show full year
                date_str = str(trans.get('transaction_date', trans.get('borrow_date', trans.get('return_date', ''))))
                if date_str and date_str != 'None':
                    try:
                        from datetime import datetime
                        if isinstance(date_str, str) and len(date_str) >= 10:
                            date_obj = datetime.strptime(str(date_str)[:10], '%Y-%m-%d')
                            date_str = date_obj.strftime('%b %d, %Y')  # Full year
                    except:
                        pass
                date_label = QLabel(date_str if date_str and date_str != 'None' else 'N/A')
                date_label.setFont(QFont('Inter', 10))
                date_label.setStyleSheet('color: #666;')
                date_label.setFixedWidth(120)
                date_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                row_layout.addWidget(date_label)

                # Member
                member_label = QLabel(trans.get('member_name', 'N/A'))
                member_label.setFont(QFont('Inter', 10))
                member_label.setStyleSheet('color: #333;')
                member_label.setFixedWidth(180)
                member_label.setWordWrap(True)
                row_layout.addWidget(member_label)

                # Book
                book_label = QLabel(trans.get('book_title', 'N/A'))
                book_label.setFont(QFont('Inter', 10))
                book_label.setStyleSheet('color: #333;')
                book_label.setFixedWidth(280)
                book_label.setWordWrap(True)
                row_layout.addWidget(book_label)

                # Librarian - FIXED to show actual names
                librarian = trans.get('librarian_name', trans.get('processed_by_name', 'System'))
                if not librarian or librarian == 'None' or librarian == 'SYSTEM':
                    # Try to get from transaction type to determine actual librarian
                    if trans.get('status') == 'Borrowed' and trans.get('processed_by_name'):
                        librarian = trans.get('processed_by_name')
                    else:
                        librarian = 'System'
                librarian_label = QLabel(str(librarian))
                librarian_label.setFont(QFont('Inter', 10))
                librarian_label.setStyleSheet('color: #666;')
                librarian_label.setFixedWidth(180)
                librarian_label.setWordWrap(True)
                row_layout.addWidget(librarian_label)

                # Status - FIXED to show full text
                status = trans.get('status', trans.get('transaction_status', 'N/A'))
                if status == 'Borrowed':
                    display_status = 'Borrowed'
                    status_color = '#FF9800'
                elif status == 'Returned':
                    display_status = 'Returned'
                    status_color = '#4CAF50'
                else:
                    display_status = status
                    status_color = '#666'

                status_label = QLabel(display_status)
                status_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
                status_label.setStyleSheet(f'color: {status_color};')
                status_label.setFixedWidth(100)
                status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                row_layout.addWidget(status_label)

                # Overdue Fee
                fee = trans.get('overdue_fee', 0)
                if fee and fee > 0:
                    fee_str = f"₱{fee}"
                    fee_color = '#F44336'
                else:
                    fee_str = "-"
                    fee_color = '#999'

                fee_label = QLabel(fee_str)
                fee_label.setFont(QFont('Inter', 10))
                fee_label.setStyleSheet(f'color: {fee_color};')
                fee_label.setFixedWidth(100)
                fee_label.setAlignment(Qt.AlignmentFlag.AlignRight)
                row_layout.addWidget(fee_label)

                row_layout.addStretch()
                trans_layout.addWidget(row_widget)

            self.report_preview_layout.addWidget(trans_container)

        # ========== MEMBERS REPORT SECTION ==========
        if 'members' in report_data and report_data['members'] and len(report_data['members']) > 0:
            members = report_data['members']

            members_header = QLabel("👥 Member Report")
            members_header.setFont(QFont('Inter', 18, QFont.Weight.Bold))
            members_header.setStyleSheet('color: #1C0C4F; margin-top: 20px;')
            self.report_preview_layout.addWidget(members_header)

            members_container = QWidget()
            members_layout = QVBoxLayout(members_container)
            members_layout.setSpacing(8)

            # Member headers
            member_header_widget = QWidget()
            member_header_layout = QHBoxLayout(member_header_widget)
            member_header_layout.setContentsMargins(0, 10, 0, 10)
            member_header_layout.setSpacing(10)

            member_headers = ['Name', 'Member ID', 'Borrowed', 'Overdue', 'Status']
            member_widths = [250, 150, 150, 150, 120]

            for header, width in zip(member_headers, member_widths):
                label = QLabel(header)
                label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
                label.setStyleSheet('color: #1C0C4F;')
                label.setFixedWidth(width)
                member_header_layout.addWidget(label)

            member_header_layout.addStretch()
            members_layout.addWidget(member_header_widget)

            # Member rows
            for i, member in enumerate(members[:20]):
                member_row = QWidget()
                if i % 2 == 0:
                    member_row.setStyleSheet('background-color: #F9F9F9;')

                member_row_layout = QHBoxLayout(member_row)
                member_row_layout.setContentsMargins(0, 8, 0, 8)
                member_row_layout.setSpacing(10)

                # Name
                name_label = QLabel(member.get('name', 'N/A'))
                name_label.setFont(QFont('Inter', 10))
                name_label.setFixedWidth(250)
                name_label.setWordWrap(True)
                member_row_layout.addWidget(name_label)

                # Member ID
                id_label = QLabel(member.get('member_id', 'N/A'))
                id_label.setFont(QFont('Inter', 10))
                id_label.setFixedWidth(150)
                member_row_layout.addWidget(id_label)

                # ===== REPLACE THESE LINES =====
                # Borrowed count - show total borrowed
                borrowed = str(member.get('borrowed', member.get('borrowed_count', 0)))
                borrowed_label = QLabel(borrowed)
                borrowed_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
                borrowed_label.setFixedWidth(100)
                borrowed_label.setStyleSheet('color: #336DED;')
                borrowed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                member_row_layout.addWidget(borrowed_label)

                # Overdue count - show current overdue count
                overdue = int(member.get('overdue', member.get('overdue_count', 0)))
                overdue_label = QLabel(str(overdue))
                overdue_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
                overdue_label.setFixedWidth(100)
                if overdue > 0:
                    overdue_label.setStyleSheet('color: #F44336; font-weight: bold;')
                overdue_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                member_row_layout.addWidget(overdue_label)
                # ===============================

                # Status
                status = "⚠️ Overdue" if overdue > 0 else "✅ Active"
                status_label = QLabel(status)
                status_label.setFont(QFont('Inter', 10))
                status_label.setFixedWidth(120)
                status_label.setStyleSheet('color: #F44336;' if overdue > 0 else 'color: #4CAF50;')
                status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                member_row_layout.addWidget(status_label)

                member_row_layout.addStretch()
                members_layout.addWidget(member_row)

            self.report_preview_layout.addWidget(members_container)

        # ========== BOOKS REPORT SECTION ==========
        if 'books' in report_data and report_data['books'] and len(report_data['books']) > 0:
            books = report_data['books']

            books_header = QLabel("📚 Book Inventory Report")
            books_header.setFont(QFont('Inter', 18, QFont.Weight.Bold))
            books_header.setStyleSheet('color: #1C0C4F; margin-top: 20px;')
            self.report_preview_layout.addWidget(books_header)

            books_container = QWidget()
            books_layout = QVBoxLayout(books_container)
            books_layout.setSpacing(8)

            # Book headers - INCREASED STATUS WIDTH
            book_header_widget = QWidget()
            book_header_layout = QHBoxLayout(book_header_widget)
            book_header_layout.setContentsMargins(0, 10, 0, 10)
            book_header_layout.setSpacing(10)

            book_headers = ['Title', 'Author', 'Available', 'Total', 'Location', 'Status']
            book_widths = [280, 200, 100, 100, 150, 120]  # Status increased to 120

            for header, width in zip(book_headers, book_widths):
                label = QLabel(header)
                label.setFont(QFont('Inter', 11, QFont.Weight.Bold))
                label.setStyleSheet('color: #1C0C4F;')
                label.setFixedWidth(width)
                book_header_layout.addWidget(label)

            book_header_layout.addStretch()
            books_layout.addWidget(book_header_widget)

            # Book rows
            for i, book in enumerate(books[:20]):
                book_row = QWidget()
                if i % 2 == 0:
                    book_row.setStyleSheet('background-color: #F9F9F9;')

                book_row_layout = QHBoxLayout(book_row)
                book_row_layout.setContentsMargins(0, 8, 0, 8)
                book_row_layout.setSpacing(10)

                # Title
                title_label = QLabel(book.get('title', 'N/A'))
                title_label.setFont(QFont('Inter', 10))
                title_label.setFixedWidth(280)
                title_label.setWordWrap(True)
                book_row_layout.addWidget(title_label)

                # Author
                author_label = QLabel(book.get('author', 'N/A'))
                author_label.setFont(QFont('Inter', 10))
                author_label.setFixedWidth(200)
                author_label.setWordWrap(True)
                book_row_layout.addWidget(author_label)

                # Available
                available = str(book.get('available_copies', 0))
                available_label = QLabel(available)
                available_label.setFont(QFont('Inter', 10, QFont.Weight.Bold))
                available_label.setFixedWidth(80)
                available_label.setStyleSheet('color: #4CAF50;' if int(available) > 0 else 'color: #999;')
                available_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                book_row_layout.addWidget(available_label)

                # Total
                total_label = QLabel(str(book.get('total_copies', 0)))
                total_label.setFont(QFont('Inter', 10))
                total_label.setFixedWidth(80)
                total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                book_row_layout.addWidget(total_label)

                # Location
                location_label = QLabel(book.get('location', 'N/A'))
                location_label.setFont(QFont('Inter', 10))
                location_label.setFixedWidth(150)
                location_label.setWordWrap(True)
                book_row_layout.addWidget(location_label)

                # Status - UPDATED WIDTH TO 120
                status = "Available" if int(book.get('available_copies', 0)) > 0 else "Not Available"
                status_label = QLabel(status)
                status_label.setFont(QFont('Inter', 10))
                status_label.setFixedWidth(120)  # Match header width
                status_label.setStyleSheet('color: #4CAF50;' if status == "Available" else 'color: #FF9800;')
                status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                book_row_layout.addWidget(status_label)

                book_row_layout.addStretch()
                books_layout.addWidget(book_row)

            self.report_preview_layout.addWidget(books_container)

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