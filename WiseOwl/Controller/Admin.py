# Controller/Admin.py
from Model.DatabaseHandler import DatabaseHandler


class AdminController:
    def __init__(self, user_name, member_id, role):
        self.user_name = user_name
        self.member_id = member_id
        self.role = role

        self.db_handler = DatabaseHandler()
        self.db_handler.connect()

        self.current_view = None
        self.logout_callback = None

    # MAIN VIEW NAVIGATION

    def show_dashboard(self):
        """Show admin dashboard"""
        from View.AdminDashboard import AdminDashboardView
        self._switch_view(AdminDashboardView)
        self._setup_dashboard()

    def show_inventory(self):
        """Show inventory management"""
        from View.AdminInventory import AdminInventoryView
        self._switch_view(AdminInventoryView)
        self._setup_inventory()

    def show_circulation(self):
        """Show circulation management"""
        from View.AdminCirculation import AdminCirculationView
        self._switch_view(AdminCirculationView)
        self._setup_circulation()

    def show_members(self):
        """Show member management"""
        from View.AdminMembers import AdminMembersView
        self._switch_view(AdminMembersView)
        self._setup_members()

    def show_reports(self):
        """Show reports view"""
        from View.AdminReports import AdminReportsView
        self._switch_view(AdminReportsView)
        self._setup_reports()

    # ========== _switch_view METHOD ==========

    def _switch_view(self, view_class):
        """Switch to a new view"""
        # Don't do anything if we're already on this view
        if self.current_view and self.current_view.__class__ == view_class:
            # Just bring to front if already exists
            self.current_view.show()
            self.current_view.raise_()
            self.current_view.activateWindow()
            return

        # Store old view reference
        old_view = self.current_view

        # Create new view
        try:
            self.current_view = view_class(self.user_name, self.member_id, self.role)
        except Exception as e:
            print(f"Error creating view: {e}")
            # If new view creation fails, keep the old one
            self.current_view = old_view
            if old_view:
                old_view.show()
                old_view.raise_()
            return

        # Show the new view FIRST
        self.current_view.show()
        self.current_view.raise_()
        self.current_view.activateWindow()

        # Then close the old view AFTER the new one is visible
        if old_view and old_view != self.current_view:
            try:
                old_view.close()
            except:
                pass

    # SETUP METHODS

    def _setup_dashboard(self):
        """Setup dashboard view callbacks"""
        if not self.current_view:
            return

        self.current_view.controller = self

        self.current_view.dashboard_callback = self.show_dashboard
        self.current_view.inventory_callback = self.show_inventory
        self.current_view.circulation_callback = self.show_circulation
        self.current_view.members_callback = self.show_members
        self.current_view.reports_callback = self.show_reports
        self.current_view.logout_callback = self.handle_logout
        self.current_view.checkout_callback = self.handle_checkout
        self.current_view.checkin_callback = self.handle_checkin

        # Get fresh data
        stats = self.get_library_stats()
        overdue_books = self.get_overdue_books()

        # Debug print
        print(f"\n📊 Dashboard Setup:")
        print(f"   Stats: {stats}")
        print(f"   Overdue books count: {len(overdue_books)}")
        for book in overdue_books:
            print(f"      - {book}")

        # Update the view
        self.current_view.update_stats(stats)
        self.current_view.update_overdue_books(overdue_books)

    def _setup_inventory(self):
        """Setup inventory view callbacks"""
        if not self.current_view:
            return

        self.current_view.dashboard_callback = self.show_dashboard
        self.current_view.inventory_callback = self.show_inventory
        self.current_view.circulation_callback = self.show_circulation
        self.current_view.members_callback = self.show_members
        self.current_view.reports_callback = self.show_reports
        self.current_view.logout_callback = self.handle_logout

        self.current_view.search_book_callback = self.handle_search_books
        self.current_view.filter_book_callback = self.handle_filter_books
        self.current_view.add_book_callback = self.handle_add_book
        self.current_view.edit_book_callback = self.handle_edit_book
        self.current_view.delete_book_callback = self.handle_delete_book

        books = self.get_all_books()
        self.current_view.update_books(books)

    def _setup_circulation(self):
        """Setup circulation view callbacks"""
        if not self.current_view:
            return

        self.current_view.dashboard_callback = self.show_dashboard
        self.current_view.inventory_callback = self.show_inventory
        self.current_view.circulation_callback = self.show_circulation
        self.current_view.members_callback = self.show_members
        self.current_view.reports_callback = self.show_reports
        self.current_view.logout_callback = self.handle_logout
        self.current_view.checkout_callback = self.handle_checkout
        self.current_view.checkin_callback = self.handle_checkin

        self.current_view.update_stats(self.get_library_stats())

    def _setup_members(self):
        """Setup members view callbacks"""
        if not self.current_view:
            return

        self.current_view.dashboard_callback = self.show_dashboard
        self.current_view.inventory_callback = self.show_inventory
        self.current_view.circulation_callback = self.show_circulation
        self.current_view.members_callback = self.show_members
        self.current_view.reports_callback = self.show_reports
        self.current_view.logout_callback = self.handle_logout

        # Connect controller to view
        self.current_view.controller = self

        # Connect member CRUD callbacks
        self.current_view.add_member_callback = self.add_member
        self.current_view.edit_member_callback = self.update_member
        self.current_view.search_member_callback = self.handle_search_members
        self.current_view.delete_member_callback = self.handle_delete_member

        self.current_view.update_members_list(self.get_all_users())

    def _setup_reports(self):
        """Setup reports view callbacks"""
        if not self.current_view:
            return

        self.current_view.dashboard_callback = self.show_dashboard
        self.current_view.inventory_callback = self.show_inventory
        self.current_view.circulation_callback = self.show_circulation
        self.current_view.members_callback = self.show_members
        self.current_view.reports_callback = self.show_reports
        self.current_view.logout_callback = self.handle_logout

        # Connect controller to view
        self.current_view.controller = self

        # Connect both callbacks
        self.current_view.generate_report_callback = self.handle_generate_report
        self.current_view.export_pdf_callback = self.handle_export_pdf

        # Pre-load data for the default report type
        if hasattr(self.current_view, 'selected_report_type'):
            report_data = self.get_report_data(self.current_view.selected_report_type)
            self.current_view.update_report_preview(report_data)

    # ========== DATABASE OPERATIONS ==========

    def get_library_stats(self):
        """Get library statistics from database"""
        stats = self.db_handler.get_library_stats()
        if not stats:
            return []
        return self._format_stats(stats)

    def get_overdue_books(self):
        """Get overdue books from database"""
        overdue_books = self.db_handler.get_overdue_books()
        if not overdue_books:
            return []
        return self._format_overdue_books(overdue_books)

    def get_all_books(self):
        """Get all books from database"""
        books_data = self.db_handler.get_all_books()
        if not books_data:
            return []
        return self._format_books(books_data)

    def get_all_users(self):
        """Get all users from database"""
        users_data = self.db_handler.get_all_users()
        return self._format_users(users_data) if users_data else []

    def search_books(self, query):
        """Search books in database"""
        if not query:
            return self.get_all_books()

        books_data = self.db_handler.search_books(query)
        return self._format_books(books_data) if books_data else []

    def search_members(self, query):
        """Search members in database"""
        try:
            if not query or not query.strip():
                return self.get_all_users()

            # Check if db_handler is connected
            if not self.db_handler.is_connected:
                self.db_handler.connect()

            members_data = self.db_handler.search_members(query.strip())
            return self._format_users(members_data) if members_data else []
        except Exception as e:
            print(f"Error in search_members: {e}")
            import traceback
            traceback.print_exc()
            return []

    def checkout_book(self, member_id, book_id):
        """Process book checkout - uses book ID (called internally)"""
        if not member_id or not book_id:
            return False, "Please enter both Member ID and Book ID", None

        return self.db_handler.process_checkout(member_id, book_id)

    def checkin_book(self, member_id, book_id, condition):
        """Process book checkin - Now with member_id"""
        if not book_id:
            return False, "Please enter Book ID"

        if not member_id:
            return False, "Please enter Member ID"

        return self.db_handler.process_checkin(member_id, book_id, condition)
    # ========== UI HANDLERS ==========

    def handle_checkout(self, member_id, book_title):
        """Handle checkout UI event - NOW WITH LIBRARIAN INFO"""
        if not self._confirm_action("Check Out", f"Check out book '{book_title}' to member {member_id}?"):
            return

        # First, find the book by title
        book = self.find_book_by_title(book_title)

        if not book:
            self._show_message(
                "Checkout Failed",
                f"Book '{book_title}' not found in the library catalog.",
                "error"
            )
            return

        book_id = book['book_id']  # Get the actual book ID

        # Get result from database handler WITH LIBRARIAN INFO
        result = self.db_handler.process_checkout(
            member_id,
            book_id,
            librarian_id=self.member_id,  # Pass librarian ID
            librarian_name=self.user_name  # Pass librarian name
        )

        if isinstance(result, tuple) and len(result) == 3:
            success, message, receipt_data = result
        else:
            # Fallback for backward compatibility
            success, message = result
            receipt_data = None

        if success:
            # Add librarian information to receipt data
            if receipt_data:
                receipt_data['librarian_name'] = self.user_name
                receipt_data['librarian_id'] = self.member_id

            # Show success message
            self._show_result("Checkout", success, message)

            # Show receipt dialog if we have receipt data and the view has the method
            if receipt_data and hasattr(self.current_view, 'show_receipt'):
                self.current_view.show_receipt(receipt_data, self.user_name, self.member_id)

            self._refresh_current_view()
        else:
            self._show_result("Checkout", success, message)

    def handle_checkin(self, member_id, book_title, condition):
        """Handle checkin UI event - NOW WITH LIBRARIAN INFO"""
        print(f"Handling checkin - Member: {member_id}, Book Title: {book_title}, Condition: {condition}")

        if not self._confirm_action("Check In",
                                    f"Check in book '{book_title}' from member {member_id} with condition: {condition}?"):
            return

        try:
            # First, find the book by title
            book = self.find_book_by_title(book_title)

            if not book:
                self._show_message(
                    "Checkin Failed",
                    f"Book '{book_title}' not found in the library catalog.",
                    "error"
                )
                return

            book_id = book['book_id']  # Get the actual book ID

            # Get the borrow record details first to check if overdue
            borrow_record = self.db_handler.get_borrow_record(member_id, book_id)

            if borrow_record and borrow_record.get('status') == 'Borrowed':
                # Check if overdue
                from datetime import date
                due_date = borrow_record.get('due_date')
                if due_date and due_date < date.today():
                    days_overdue = (date.today() - due_date).days

                    # Get book and member details for receipt
                    book_details = self.db_handler.get_book_by_id(book_id)
                    member_details = self.db_handler.get_member_details(member_id)

                    # Prepare check-in data with overdue info
                    checkin_data = {
                        'transaction_id': f"CI-{date.today().strftime('%Y%m%d')}-{book_id}-{member_id}",
                        'librarian_name': self.user_name,
                        'librarian_id': self.member_id,
                        'member_name': member_details.get('user_name') if member_details else 'Unknown',
                        'member_id': member_id,
                        'book_title': book['title'],
                        'book_id': book_id,
                        'book_author': book_details.get('author') if book_details else 'Unknown',
                        'condition': condition,
                        'borrow_date': borrow_record.get('borrow_date').strftime("%b %d, %Y") if borrow_record.get(
                            'borrow_date') else 'N/A',
                        'due_date': borrow_record.get('due_date').strftime("%b %d, %Y") if borrow_record.get(
                            'due_date') else 'N/A',
                        'return_date': date.today().strftime("%b %d, %Y"),
                        'days_overdue': days_overdue
                    }

                    # Show overdue dialog with fee calculation
                    self._show_overdue_checkin_dialog(checkin_data, member_id, book_id, condition)
                    return

            # If not overdue, process normal checkin WITH LIBRARIAN INFO
            success, message = self.db_handler.process_checkin(
                member_id,
                book_id,
                condition,
                librarian_id=self.member_id,
                librarian_name=self.user_name
            )

            if success:
                # Get book and member details for receipt
                book_details = self.db_handler.get_book_by_id(book_id)
                member_details = self.db_handler.get_member_details(member_id)

                # Prepare check-in data for receipt
                from datetime import date
                checkin_data = {
                    'transaction_id': f"CI-{date.today().strftime('%Y%m%d')}-{book_id}-{member_id}",
                    'librarian_name': self.user_name,
                    'librarian_id': self.member_id,
                    'member_name': member_details.get('user_name') if member_details else 'Unknown',
                    'member_id': member_id,
                    'book_title': book['title'],
                    'book_id': book_id,
                    'book_author': book_details.get('author') if book_details else 'Unknown',
                    'condition': condition,
                    'borrow_date': borrow_record.get('borrow_date').strftime(
                        "%b %d, %Y") if borrow_record and borrow_record.get('borrow_date') else 'N/A',
                    'due_date': borrow_record.get('due_date').strftime(
                        "%b %d, %Y") if borrow_record and borrow_record.get(
                        'due_date') else 'N/A',
                    'return_date': date.today().strftime("%b %d, %Y")
                }

                # Show checkin receipt
                if hasattr(self.current_view, 'show_checkin_receipt'):
                    self.current_view.show_checkin_receipt(checkin_data)

                self._show_result("Checkin", success, message)
                self._refresh_current_view()
            else:
                self._show_result("Checkin", success, message)

        except Exception as e:
            print(f"Error in handle_checkin: {e}")
            import traceback
            traceback.print_exc()
            self._show_message("Error", f"An error occurred: {str(e)}", "error")

    def _show_overdue_checkin_dialog(self, checkin_data, member_id, book_id, condition):
        """Show overdue checkin dialog with fee calculation"""
        try:
            from View.Dialogs import CheckinDueDialog

            # Create and show the overdue dialog
            dialog = CheckinDueDialog(checkin_data, self.current_view)
            result = dialog.exec()

            # Check result (0 = Rejected, 1 = Accepted)
            if result == 0:  # Rejected (Close button clicked)
                self._show_message("Checkin Cancelled", "Overdue checkin was cancelled.", "info")
                return

            # Process the checkin
            success, message = self.checkin_book(member_id, book_id, condition)

            if success:
                self._show_result("Checkin", success, f"{message} (Overdue fee of {dialog.total_fee} applies)")
                self._refresh_current_view()
            else:
                self._show_result("Checkin", success, message)

        except ImportError as e:
            print(f"Import error in overdue dialog: {e}")
            self._show_message("Error", "Could not load the overdue dialog.", "error")
        except Exception as e:
            print(f"Error in overdue dialog: {e}")
            import traceback
            traceback.print_exc()
            self._show_message("Error", f"An error occurred: {str(e)}", "error")

    def find_book_by_title(self, title):
        """Find a book by its title (exact or partial match)"""
        try:
            # Search for books matching the title
            books = self.search_books(title)

            if not books:
                return None

            # If multiple books found with similar titles, you might want to handle that
            # For now, return the first match
            if len(books) > 1:
                # Optional: Show selection dialog if multiple books found
                print(f"Multiple books found for title '{title}'. Using first match: {books[0]['title']}")

            return books[0] if books else None

        except Exception as e:
            print(f"Error finding book by title: {e}")
            return None

    def handle_search_books(self, query):
        """Handle book search UI event"""
        results = self.search_books(query)

        if hasattr(self.current_view, 'update_books'):
            self.current_view.update_books(results)

        if not results:
            self._show_message("No Results", f"No books found for: {query}", "info")

    def handle_book_title_search(self, title, search_type):
        """Handle book search by title for circulation"""
        print(f"Searching for book title: {title} for {search_type}")

        if not title:
            return

        # Search for books matching the title
        books = self.search_books(title)

        # Format for circulation view
        formatted_books = []
        for book in books:
            formatted_books.append({
                "book_id": book.get("book_id"),
                "title": book.get("title"),
                "author": book.get("author"),
                "available_copies": book.get("available_copies", 0)
            })

        # Send results back to view
        if hasattr(self.current_view, 'show_book_search_results'):
            self.current_view.show_book_search_results(formatted_books, search_type)


    def _setup_circulation(self):
        """Setup circulation view callbacks"""
        if not self.current_view:
            return

        self.current_view.dashboard_callback = self.show_dashboard
        self.current_view.inventory_callback = self.show_inventory
        self.current_view.circulation_callback = self.show_circulation
        self.current_view.members_callback = self.show_members
        self.current_view.reports_callback = self.show_reports
        self.current_view.logout_callback = self.handle_logout
        self.current_view.checkout_callback = self.handle_checkout
        self.current_view.checkin_callback = self.handle_checkin
        self.current_view.search_callback = self.handle_search_books

        self.current_view.update_stats(self.get_library_stats())

    def handle_search_members(self, query):
        """Handle member search UI event"""
        try:
            # Check if database is connected
            if not self.db_handler.is_connected:
                self.db_handler.connect()

            results = self.search_members(query)

            if hasattr(self.current_view, 'update_members_list'):
                self.current_view.update_members_list(results)

            if not results:
                self._show_message("No Results", f"No members found for: {query}", "info")
        except Exception as e:
            print(f"Error in handle_search_members: {e}")
            import traceback
            traceback.print_exc()
            self._show_message("Search Error", f"An error occurred while searching: {str(e)}", "error")

    def handle_logout(self):
        """Handle logout"""
        if not self._confirm_action("Logout", "Are you sure you want to log out?"):
            return

        self.db_handler.close()
        if self.current_view:
            try:
                self.current_view.close()
            except:
                pass
            self.current_view = None

        if self.logout_callback:
            self.logout_callback()

    # ========== REPORTS HANDLERS ==========

    def handle_generate_report(self, report_type):
        """Handle generate report button click"""
        report_data = self.get_report_data(report_type)

        if hasattr(self.current_view, 'update_report_preview'):
            self.current_view.update_report_preview(report_data)

    def handle_export_pdf(self, report_data):
        """Handle export PDF button click"""
        if not report_data:
            if hasattr(self.current_view, 'show_message'):
                self.current_view.show_message("No Report", "Please generate a report first", "warning")
            return

        # The view handles the actual PDF export
        if hasattr(self.current_view, 'export_to_pdf'):
            self.current_view.export_to_pdf()

    def get_report_data(self, report_type):
        """Get data for reports from database - with fresh data"""

        # First, update overdue counts in the database
        self.db_handler.update_overdue_counts()

        stats = self._get_formatted_library_stats()

        # Get overdue books
        overdue_books = self.get_overdue_books()

        # Get actual data from database
        borrowed_books = self._get_borrowed_books_for_report()
        returned_books = self._get_returned_books_for_report()
        members = self.get_all_users()
        books = self.get_all_books()

        print(f"📊 Report Data - Members: {len(members)}, Books: {len(books)}, Overdue: {len(overdue_books)}")

        # Debug: Print member overdue stats
        for member in members[:5]:  # First 5 members
            print(f"   Member: {member.get('name')}, Overdue: {member.get('overdue')}")

        # Get transaction data based on report type
        if report_type == "circulation_report":
            transactions = self.db_handler.get_detailed_circulation_report("all")
            circulation_summary = self.db_handler.get_circulation_summary()
        elif report_type == "checkouts_only":
            transactions = self.db_handler.get_detailed_circulation_report("checkouts_only")
            circulation_summary = None
        elif report_type == "returns_only":
            transactions = self.db_handler.get_detailed_circulation_report("returns_only")
            circulation_summary = None
        else:
            transactions = self.db_handler.get_transaction_history(limit=200)
            circulation_summary = None

        report_data = {
            'report_type': report_type,
            'statistics': stats,
            'overdue_books': overdue_books,
            'borrowed_books': borrowed_books,
            'returned_books': returned_books,
            'members': members,
            'books': books,
            'transactions': transactions,
            'circulation_summary': circulation_summary
        }

        return report_data

    def get_transaction_history(self, limit=100):
        """Get transaction history for reports"""
        return self.db_handler.get_transaction_history(limit)

    def _refresh_current_view(self):
        """Refresh data in current view"""
        if self.current_view:
            view_name = self.current_view.__class__.__name__

            if "Dashboard" in view_name:
                self.current_view.update_stats(self.get_library_stats())
                self.current_view.update_overdue_books(self.get_overdue_books())
            elif "Inventory" in view_name:
                self.current_view.update_books(self.get_all_books())
            elif "Circulation" in view_name:
                self.current_view.update_stats(self.get_library_stats())
            elif "Members" in view_name:
                self.current_view.update_members_list(self.get_all_users())

    def _confirm_action(self, title, message):
        """Delegate confirmation to View"""
        if hasattr(self.current_view, 'show_confirmation'):
            return self.current_view.show_confirmation(title, message)
        return False

    def _show_result(self, action, success, message):
        """Delegate result display to View"""
        if success:
            self._show_message("Success", message, "info")
        else:
            self._show_message(f"{action} Failed", message, "error")

    def _show_message(self, title, message, message_type="info"):
        """Delegate message display to View"""
        if hasattr(self.current_view, 'show_message'):
            self.current_view.show_message(title, message, message_type)

    # ========== DATA FORMATTING ==========

    def _format_stats(self, stats):
        """Format statistics for UI"""
        return [
            {"title": "Total Books", "value": str(stats.get("total_books", 0)), "color": "#1C0C4F"},
            {"title": "Available", "value": str(stats.get("available_books", 0)), "color": "#4CAF50"},
            {"title": "Borrowed", "value": str(stats.get("borrowed_books", 0)), "color": "#FF9800"},
            {"title": "Total Members", "value": str(stats.get("total_members", 0)), "color": "#336DED"}
        ]

    def _format_overdue_books(self, overdue_books):
        """Format overdue books for UI"""
        print(f"\n📝 Formatting {len(overdue_books)} overdue books:")

        formatted = []
        for book in overdue_books:
            print(f"   Raw book: {book}")

            if isinstance(book, dict):
                # Handle dictionary format
                formatted.append({
                    "title": book.get("title", "Unknown"),
                    "borrower": book.get("borrower", "Unknown"),
                    "days": book.get("days_overdue", 0)
                })
            elif isinstance(book, tuple) and len(book) >= 3:
                # Handle tuple format
                formatted.append({
                    "title": book[0],
                    "borrower": book[1],
                    "days": book[2]
                })

        print(f"   Formatted: {formatted}")
        return formatted

    def _format_books(self, books_data):
        """Format books for UI"""
        formatted_books = []

        if not books_data:
            return formatted_books

        for book in books_data:
            if isinstance(book, dict):
                # Database returns dictionaries
                formatted_books.append({
                    "book_id": str(book.get('id', '')),
                    "title": book.get('title', 'Unknown Title'),
                    "author": book.get('author', 'Unknown Author'),
                    "genre": book.get('genre', 'No Genre'),
                    "total_copies": int(book.get('total_copies', 0)),
                    "available_copies": int(book.get('available_copies', 0)),
                    "location": book.get('location', 'No Location'),
                    "description": book.get('description', '')
                })
            elif isinstance(book, tuple):
                if len(book) >= 8:
                    formatted_books.append({
                        "book_id": str(book[0]) if book[0] else "",
                        "title": str(book[1]) if book[1] else "Unknown Title",
                        "author": str(book[2]) if book[2] else "Unknown Author",
                        "genre": str(book[3]) if book[3] else "No Genre",
                        "total_copies": int(book[4]) if book[4] is not None else 0,
                        "available_copies": int(book[5]) if book[5] is not None else 0,
                        "location": str(book[6]) if book[6] else "No Location",
                        "description": str(book[7]) if book[7] else ""
                    })

        return formatted_books

    def _format_users(self, users_data):
        """Format users for UI - with proper overdue counts"""
        formatted_users = []

        if not users_data:
            return formatted_users

        for user in users_data:
            if isinstance(user, dict):
                # Database returns dictionaries
                overdue = int(user.get('overdue_count', 0))
                borrowed = int(user.get('borrowed_count', 0))
                currently_borrowed = int(user.get('currently_borrowed', 0))

                formatted_users.append({
                    "name": user.get('user_name', 'Unknown Member'),
                    "email": user.get('email', 'No email'),
                    "join_date": str(user.get('join_date', 'N/A')),
                    "borrowed": borrowed,
                    "overdue": overdue,
                    "currently_borrowed": currently_borrowed,
                    "member_id": user.get('member_id', ''),
                    "status": "⚠️ Overdue" if overdue > 0 else "✅ Active"
                })
            elif isinstance(user, tuple):
                # Fallback for tuple format
                overdue = int(user[4]) if len(user) > 4 else 0
                borrowed = int(user[3]) if len(user) > 3 else 0

                formatted_users.append({
                    "name": user[0] if len(user) > 0 else "Unknown Member",
                    "email": user[1] if len(user) > 1 else "No email",
                    "join_date": str(user[2]) if len(user) > 2 else "N/A",
                    "borrowed": borrowed,
                    "overdue": overdue,
                    "currently_borrowed": 0,
                    "member_id": user[5] if len(user) > 5 else "",
                    "status": "⚠️ Overdue" if overdue > 0 else "✅ Active"
                })

        return formatted_users

    def _get_formatted_library_stats(self):
        """Get formatted library statistics"""
        stats = self.db_handler.get_library_stats()
        if not stats:
            return {
                'Total Books': '0',
                'Available Books': '0',
                'Borrowed Books': '0',
                'Total Members': '0'
            }

        print(f"📊 Formatting stats: {stats}")  # Debug print

        return {
            'Total Books': str(stats.get('total_books', 0)),
            'Available Books': str(stats.get('available_books', 0)),
            'Borrowed Books': str(stats.get('borrowed_books', 0)),
            'Total Members': str(stats.get('total_members', 0))
        }

    # ========== BOOK CRUD HANDLERS ==========

    def handle_filter_books(self, filter_text):
        """Handle book filtering"""
        all_books = self.get_all_books()

        if filter_text == "All Books":
            filtered_books = all_books
        elif filter_text == "Available Only":
            filtered_books = [book for book in all_books if book.get("available_copies", 0) > 0]
        elif filter_text == "Borrowed Only":
            filtered_books = [book for book in all_books if book.get("available_copies", 0) == 0]
        else:
            filtered_books = all_books

        if hasattr(self.current_view, 'update_books'):
            self.current_view.update_books(filtered_books)

    def handle_add_book(self, book_data):
        """Handle add book from UI"""
        success, message = self.add_book(book_data)
        self._show_result("Add Book", success, message)

        if success:
            self._refresh_current_view()

    def handle_edit_book(self, book_data):
        """Handle edit book from UI"""
        success, message = self.edit_book(book_data)
        self._show_result("Edit Book", success, message)

        if success:
            self._refresh_current_view()

    def handle_delete_book(self, book_id):
        """Handle delete book from UI"""
        if not self._confirm_action("Delete Book",
                                    f"Are you sure you want to delete this book? This action cannot be undone."):
            return

        success, message = self.delete_book(book_id)
        self._show_result("Delete Book", success, message)

        if success:
            self._refresh_current_view()

    # ========== BOOK CRUD METHODS ==========

    def add_book(self, book_data):
        """Add new book to database"""
        if not book_data.get('title') or not book_data.get('author'):
            return False, "Title and author are required"

        if book_data.get('total_copies', 0) < 1:
            return False, "Total copies must be at least 1"

        if 'available_copies' not in book_data:
            book_data['available_copies'] = book_data.get('total_copies', 1)

        success, message = self.db_handler.add_book(book_data)

        if success:
            self._refresh_current_view()

        return success, message

    def edit_book(self, book_data):
        """Edit existing book"""
        book_id = book_data.get('book_id')
        if not book_id:
            return False, "Book ID is required"

        if not book_data.get('title') or not book_data.get('author'):
            return False, "Title and author are required"

        if book_data.get('total_copies', 0) < 1:
            return False, "Total copies must be at least 1"

        if book_data.get('available_copies', 0) > book_data.get('total_copies', 0):
            book_data['available_copies'] = book_data.get('total_copies')

        success, message = self.db_handler.update_book(book_id, book_data)

        if success:
            self._refresh_current_view()

        return success, message

    def delete_book(self, book_id):
        """Delete book from database"""
        if not book_id:
            return False, "Book ID is required"

        success, message = self.db_handler.delete_book(book_id)

        if success:
            self._refresh_current_view()

        return success, message

    # ========== MEMBER CRUD OPERATIONS ==========

    def add_member(self, member_data):
        """Add new member to database"""
        if not member_data.get('name') or not member_data.get('member_id'):
            return False, "Name and Member ID are required"

        if not member_data.get('email'):
            return False, "Email is required"

        success, message = self.db_handler.add_member(member_data)

        if success:
            self._refresh_current_view()

        return success, message

    def update_member(self, member_id, member_data):
        """Update existing member"""
        if not member_id:
            return False, "Member ID is required"

        if not member_data.get('name') or not member_data.get('email'):
            return False, "Name and Email are required"

        success, message = self.db_handler.update_member(member_id, member_data)

        if success:
            self._refresh_current_view()

        return success, message

    def delete_member(self, member_id):
        """Delete member from database"""
        if not member_id:
            return False, "Member ID is required"

        success, message = self.db_handler.delete_member(member_id)

        if success:
            self._refresh_current_view()

        return success, message

    def get_member_info(self, member_id):
        """Get member details"""
        return self.db_handler.get_member_details(member_id)

    # ========== MEMBER DIALOG HANDLERS ==========

    def handle_delete_member(self, member_id):
        """Handle delete member"""
        if not self._confirm_action("Delete Member", f"Are you sure you want to delete member {member_id}?"):
            return

        success, message = self.delete_member(member_id)
        self._show_result("Delete Member", success, message)

    # ========== REPORT DATA METHODS ==========

    def _get_borrowed_books_for_report(self):
        """Get borrowed books data for reports from database"""
        try:
            return self.db_handler.get_current_borrowed_books()
        except:
            # Return empty list if method not implemented or error
            return []

    def _get_returned_books_for_report(self):
        """Get returned books data for reports from database"""
        try:
            return self.db_handler.get_recent_returned_books()
        except:
            # Return empty list if method not implemented or error
            return []