# Controller/UserController.py
import sys
from Model.DatabaseHandler import DatabaseHandler

class UserController:
    def __init__(self, user_name, member_id, role, db_handler=None):
        self.user_name = user_name
        self.member_id = member_id
        self.role = role
        self.db = db_handler
        self.current_window = None
        self.logout_callback = None

        # For catalog functionality
        self.cart_items = []  # Store book IDs in cart

    def show_my_books(self):
        """Show my books view"""
        from View.UserMyBooks import UserMyBooksView

        if self.current_window:
            self.current_window.close()

        mybooks = UserMyBooksView(
            self.user_name,
            self.member_id,
            self.role
        )

        # Setup navigation callbacks
        mybooks.mybooks_callback = self.show_my_books
        mybooks.history_callback = self.show_history
        mybooks.catalog_callback = self.show_catalog
        mybooks.help_callback = self.show_help
        mybooks.logout_callback = self.handle_logout

        # Load data
        mybooks.update_books(self.get_user_books())

        mybooks.show()
        self.current_window = mybooks

    def show_history(self):
        """Show history view"""
        from View.UserHistory import UserHistoryView

        if self.current_window:
            self.current_window.close()

        history = UserHistoryView(
            self.user_name,
            self.member_id,
            self.role
        )

        # Setup navigation callbacks
        history.mybooks_callback = self.show_my_books
        history.history_callback = self.show_history
        history.catalog_callback = self.show_catalog
        history.help_callback = self.show_help
        history.logout_callback = self.handle_logout

        # Load data
        history.update_history(self.get_borrowing_history())

        history.show()
        self.current_window = history

    def show_catalog(self):
        """Show catalog view"""
        from View.UserCatalog import UserCatalogView

        if self.current_window:
            self.current_window.close()

        catalog = UserCatalogView(
            self.user_name,
            self.member_id,
            self.role
        )

        # Setup navigation callbacks
        catalog.mybooks_callback = self.show_my_books
        catalog.history_callback = self.show_history
        catalog.catalog_callback = self.show_catalog
        catalog.help_callback = self.show_help
        catalog.logout_callback = self.handle_logout

        # Setup catalog-specific callbacks
        catalog.search_callback = self.search_books
        catalog.filter_callback = self.filter_books
        catalog.borrow_callback = self.borrow_book
        catalog.view_details_callback = self.view_book_details
        catalog.cart_callback = self.show_cart

        # Load catalog data
        catalog.update_books(self.get_catalog_books())

        catalog.show()
        self.current_window = catalog

    def show_help(self):
        """Show help view"""
        from View.UserHelp import UserHelpView

        if self.current_window:
            self.current_window.close()

        help_view = UserHelpView(
            self.user_name,
            self.member_id,
            self.role
        )

        # Setup navigation callbacks
        help_view.mybooks_callback = self.show_my_books
        help_view.history_callback = self.show_history
        help_view.catalog_callback = self.show_catalog
        help_view.help_callback = self.show_help
        help_view.logout_callback = self.handle_logout

        # Load help content
        help_view.update_help_content(self.get_help_sections())

        help_view.show()
        self.current_window = help_view

    def handle_logout(self):
        """Handle logout"""
        if self.current_window:
            self.current_window.close()
            self.current_window = None

        # Call back to auth controller
        if self.logout_callback:
            self.logout_callback()

    # DATABASE-CONNECTED CATALOG METHODS
    def search_books(self, query):
        """Handle book search from database"""
        print(f"Searching for: {query}")

        books = []

        if self.db and self.db.conn:
            try:
                # Use the search_books method from DatabaseHandler
                db_results = self.db.search_books(query)

                for result in db_results:
                    # Results are dictionaries because cursor(dictionary=True)
                    books.append({
                        "book_id": str(result['id']),
                        "title": result['title'],
                        "author": result['author'],
                        "status": "Available" if result['available_copies'] > 0 else "Borrowed",
                        "genre": result.get('genre') or "Unknown",
                        "description": result.get('description') or "No description available",
                        "available_copies": result['available_copies'],
                        "location": result.get('location') or "Not specified"
                    })
            except Exception as e:
                print(f"Error searching books: {e}")
                self._show_database_error()
        else:
            self._show_database_error()

        # Update the catalog view
        if hasattr(self.current_window, 'update_books'):
            self.current_window.update_books(books, search_query=query)

    def filter_books(self, filter_text):
        """Handle book filtering"""
        print(f"Filtering by: {filter_text}")

        all_books = self.get_catalog_books()

        if filter_text == "All Books":
            filtered_books = all_books
        elif filter_text == "Available Only":
            filtered_books = [book for book in all_books if book.get("status") == "Available"]
        else:
            # Filter by genre
            filtered_books = [book for book in all_books if book.get("genre", "") == filter_text]

        # Update the catalog view
        if hasattr(self.current_window, 'update_books'):
            self.current_window.update_books(filtered_books, filter_text=filter_text)

    def borrow_book(self, book_id):
        """Handle borrowing a book with overdue check"""
        print(f"Attempting to borrow book ID: {book_id}")

        if not self.db or not self.db.conn:
            self._show_database_error()
            return False

        # Check for overdue books first
        if self.db.has_overdue_books(self.member_id):
            # Get overdue books details for the message
            try:
                query = """
                    SELECT book_title, due_date, DATEDIFF(CURDATE(), due_date) as days
                    FROM borrow_records
                    WHERE member_id = %s 
                        AND status = 'Borrowed'
                        AND due_date < CURDATE()
                """
                self.db.cursor.execute(query, (self.member_id,))
                overdue_books = self.db.cursor.fetchall()

                # Create  list of overdue books
                book_list = "\n".join([f"• {b['book_title']} (Due: {b['due_date']}, {b['days']} days overdue)"
                                       for b in overdue_books])

                error_message = (
                    f"You cannot borrow books because you have {len(overdue_books)} overdue book(s):\n\n"
                    f"{book_list}\n\n"
                    f"Please return your overdue books before borrowing new ones."
                )

                self.current_window.show_message(
                    "Borrowing Restricted",
                    error_message,
                    "warning"
                )
            except Exception as e:
                print(f"Error getting overdue details: {e}")
                self.current_window.show_message(
                    "Borrowing Restricted",
                    "You have overdue books. Please return them before borrowing new ones.",
                    "warning"
                )
            return False


        # Original borrowing logic (add to cart)
        if book_id and book_id not in self.cart_items:
            self.cart_items.append(book_id)

            # Update cart count in UI
            if hasattr(self.current_window, 'update_cart_count'):
                self.current_window.update_cart_count(len(self.cart_items))

            # Show success message
            book = next((b for b in self.get_catalog_books() if str(b.get("book_id", "")) == book_id), None)
            if book:
                self.current_window.show_message(
                    "Success",
                    f"'{book['title']}' added to cart!",
                    "info"
                )
            else:
                self.current_window.show_message(
                    "Success",
                    "Book added to cart!",
                    "info"
                )
            return True
        else:
            self.current_window.show_message(
                "Info",
                "Book already in cart!",
                "warning"
            )
            return False

    def checkout_cart(self):
        """Checkout all books in cart"""
        if not self.cart_items:
            self.current_window.show_message(
                "Empty Cart",
                "Your cart is empty!",
                "info"
            )
            return False

        # Check for overdue books before processing
        if self.db.has_overdue_books(self.member_id):
            self.current_window.show_message(
                "Borrowing Restricted",
                "You have overdue books. Please return them before borrowing new ones.",
                "warning"
            )
            return False

        # Process each book in cart
        success_count = 0
        failed_books = []

        for book_id in self.cart_items:
            success, message, _ = self.db.process_checkout(self.member_id, book_id)
            if success:
                success_count += 1
            else:
                # Find book title for better error message
                book = next((b for b in self.get_catalog_books() if str(b.get("book_id", "")) == book_id), None)
                if book:
                    failed_books.append(book['title'])
                else:
                    failed_books.append(f"Book ID: {book_id}")

        # Clear cart
        self.cart_items = []
        if hasattr(self.current_window, 'update_cart_count'):
            self.current_window.update_cart_count(0)

        # Show result message
        if success_count == len(self.cart_items):
            self.current_window.show_message(
                "Success",
                f"Successfully checked out {success_count} book(s)!",
                "info"
            )
        else:
            self.current_window.show_message(
                "Partial Success",
                f"Checked out {success_count} of {len(self.cart_items)} books.\n"
                f"Failed: {', '.join(failed_books)}",
                "warning"
            )

        return success_count > 0

    def view_book_details(self, book_id):
        """Show book details from database"""
        print(f"Viewing details for book ID: {book_id}")

        book_details = None

        if self.db and self.db.conn:
            try:
                result = self.db.get_book_by_id(book_id)
                if result:
                    # Result is a dictionary
                    book_details = {
                        "title": result['title'],
                        "author": result['author'],
                        "genre": result.get('genre') or "Unknown",
                        "status": "Available" if result['available_copies'] > 0 else "Borrowed",
                        "available_copies": result['available_copies'],
                        "total_copies": result['total_copies'],
                        "location": result.get('location') or "Not specified",
                        "description": result.get('description') or "No description available."
                    }
            except Exception as e:
                print(f"Error getting book details: {e}")

        if not book_details:
            self._show_database_error()
            return

        # Show details dialog
        if hasattr(self.current_window, 'show_book_details'):
            self.current_window.show_book_details(book_details)

    def show_cart(self):
        """Show cart view"""
        cart_count = len(self.cart_items)
        print(f"Showing cart with {cart_count} items")

        if cart_count > 0:
            cart_text = f"You have {cart_count} item(s) in your cart:\n\n"

            # Get book titles
            for i, book_id in enumerate(self.cart_items, 1):
                book = next((b for b in self.get_catalog_books() if str(b.get("book_id", "")) == book_id), None)
                if book:
                    cart_text += f"{i}. {book['title']} by {book['author']}\n"
                else:
                    cart_text += f"{i}. Book ID: {book_id}\n"

            self.current_window.show_message(
                "My Cart",
                cart_text,
                "info"
            )
        else:
            self.current_window.show_message(
                "My Cart",
                "Your cart is empty!",
                "info"
            )

    # DATA METHODS
    def get_catalog_books(self):
        """Get all books for catalog"""
        books = []

        if self.db and self.db.conn:
            try:
                # Use get_all_books method from DatabaseHandler
                db_results = self.db.get_all_books()

                for result in db_results:
                    # Results are dictionaries because cursor(dictionary=True)
                    books.append({
                        "book_id": str(result['id']),
                        "title": result['title'],
                        "author": result['author'],
                        "status": "Available" if result['available_copies'] > 0 else "Borrowed",
                        "genre": result.get('genre') or "Unknown",
                        "description": result.get('description') or "No description available",
                        "available_copies": result['available_copies'],
                        "location": result.get('location') or "Not specified"
                    })
            except Exception as e:
                print(f"Error getting catalog books: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("Database not connected!")

        return books

    def debug_borrow_records(self):
        """Direct debug of borrow_records table"""
        print(f"\n🔍 DIRECT BORROW_RECORDS DEBUG for member_id: {self.member_id}")

        if not self.db or not self.db.conn:
            print("❌ No database connection")
            return

        try:
            # 1. Check ALL borrow_records first
            print("\n1. ALL borrow_records:")
            self.db.cursor.execute("SELECT id, member_id, book_id, book_title, status FROM borrow_records")
            all_records = self.db.cursor.fetchall()

            print(f"Total records: {len(all_records)}")
            for record in all_records:
                print(f"  ID: {record['id']}, Member: {record['member_id']}, "
                      f"Book ID: {record['book_id']}, Title: {record['book_title']}, "
                      f"Status: {record['status']}")

            # 2. Check specifically for this member_id
            print(f"\n2. Records for member_id={self.member_id}:")
            self.db.cursor.execute("""
                SELECT id, book_id, book_title, status, due_date 
                FROM borrow_records 
                WHERE member_id = %s
            """, (self.member_id,))
            user_records = self.db.cursor.fetchall()

            print(f"Found {len(user_records)} records")
            for record in user_records:
                print(f"  ID: {record['id']}, Book ID: {record['book_id']}, "
                      f"Title: {record['book_title']}, Status: {record['status']}, "
                      f"Due: {record['due_date']}")

            # 3. Check status specifically
            print(f"\n3. Records with status 'Borrowed' or 'Overdue' for member_id={self.member_id}:")
            self.db.cursor.execute("""
                SELECT id, book_id, book_title, status, due_date 
                FROM borrow_records 
                WHERE member_id = %s AND status IN ('Borrowed', 'Overdue')
            """, (self.member_id,))
            active_records = self.db.cursor.fetchall()

            print(f"Found {len(active_records)} ACTIVE records")
            for record in active_records:
                print(f"  - {record['book_title']} (Status: {record['status']}, Due: {record['due_date']})")

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

    def get_borrowed_books(self):
        """Get user's currently borrowed books - FIXED with overdue detection"""
        print(f"\n🔍 get_borrowed_books() called")
        print(f"User: {self.user_name}")
        print(f"Member ID from controller: {self.member_id}")

        books = []

        if not self.db or not self.db.conn:
            print("❌ No database connection")
            return books

        try:
            # FIRST: Find correct member_id
            print(f"\n1️⃣ Finding correct member_id for '{self.user_name}'...")

            self.db.cursor.execute("""
                SELECT member_id, user_name, borrowed_count 
                FROM users 
                WHERE user_name = %s
            """, (self.user_name,))

            user_result = self.db.cursor.fetchone()

            if not user_result:
                print(f"❌ User '{self.user_name}' not found in database!")
                return books

            db_member_id = user_result['member_id']
            borrowed_count = user_result['borrowed_count']

            print(f"✅ Database says:")
            print(f"   User Name: {user_result['user_name']}")
            print(f"   Member ID: {db_member_id}")
            print(f"   Borrowed Count: {borrowed_count}")

            # Use database member_id
            actual_member_id = db_member_id

            # SECOND: Get borrow records with overdue detection IN THE SQL QUERY
            print(f"\n2️⃣ Getting borrow records for member_id='{actual_member_id}'...")

            query = """
                SELECT 
                    br.book_title,
                    b.author,
                    br.due_date,
                    br.status,
                    -- Calculate display status in SQL
                    CASE 
                        WHEN br.due_date < CURDATE() AND br.status = 'Borrowed' THEN 'Overdue'
                        ELSE br.status
                    END as display_status,
                    -- Calculate days overdue
                    CASE 
                        WHEN br.due_date < CURDATE() AND br.status = 'Borrowed' 
                        THEN DATEDIFF(CURDATE(), br.due_date)
                        ELSE 0
                    END as days_overdue
                FROM borrow_records br
                JOIN books b ON br.book_id = b.id
                WHERE br.member_id = %s 
                    AND br.status IN ('Borrowed', 'Overdue')
                ORDER BY 
                    -- Overdue first, then by due date
                    CASE 
                        WHEN br.due_date < CURDATE() THEN 0
                        ELSE 1
                    END,
                    br.due_date
            """

            self.db.cursor.execute(query, (actual_member_id,))
            results = self.db.cursor.fetchall()

            print(f"📊 Found {len(results)} borrowed books")

            for result in results:
                print(f"✅ Book: {result['book_title']}")
                print(f"   Author: {result['author']}")
                print(f"   Due: {result['due_date']}")
                print(f"   Status: {result['status']} → Display: {result['display_status']}")
                print(f"   Days overdue: {result['days_overdue']}")

                books.append({
                    "title": result['book_title'],
                    "author": result['author'],
                    "due_date": str(result['due_date']) if result['due_date'] else "No due date",
                    "status": result['display_status'],  # Use the SQL-calculated status
                    "original_status": result['status'],
                    "days_overdue": result['days_overdue']
                })

            print(f"\n🎯 FINAL: Returning {len(books)} books for {self.user_name}")
            for book in books:
                print(f"   - {book['title']} ({book['status']})")

        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()

        return books

    def get_user_stats(self):
        """Get user statistics with accurate overdue count"""
        borrowed_books = self.get_borrowed_books()
        borrowed_count = len(borrowed_books)
        overdue_count = sum(1 for book in borrowed_books if book.get("status") == "Overdue")

        return [
            {"number": str(borrowed_count), "label": "Books Borrowed", "color": "#336DED"},
            {"number": str(overdue_count), "label": "Overdue Books", "color": "#F44336"},
            {"number": str(self._get_history_count()), "label": "Reading History", "color": "#4CAF50"},
            {"number": str(len(self.cart_items)), "label": "In Cart", "color": "#FF9800"},
        ]

    def get_user_books(self):
        """Get all user's books"""
        return self.get_borrowed_books()

    def get_borrowing_history(self):
        """Get user's borrowing history"""
        history = []

        if self.db and self.db.conn:
            try:
                self.db.cursor.execute("""
                    SELECT book_title, borrow_date, return_date, status
                    FROM borrow_records 
                    WHERE member_id = %s
                    ORDER BY borrow_date DESC
                    LIMIT 20
                """, (self.member_id,))

                db_results = self.db.cursor.fetchall()
                for result in db_results:
                    # Result is a dictionary
                    history.append({
                        "title": result['book_title'],
                        "author": "Unknown",  # Need to join with books table if you want author
                        "borrowed": str(result['borrow_date']) if result['borrow_date'] else "Unknown",
                        "returned": str(result['return_date']) if result['return_date'] else "Not returned",
                        "status": result['status']
                    })
            except Exception as e:
                print(f"Error fetching borrowing history: {e}")

        return history

    def get_help_sections(self):
        """Get help content"""
        return [
            {
                "title": "Getting Started",
                "items": [
                    "Welcome to the Wise Owl Library System!",
                    "To get started, browse the catalog to find books.",
                    "You can search by title, author, or genre.",
                    "Click 'Borrow Book' to add books to your cart.",
                    "Use the cart to check out multiple books at once."
                ]
            },
            {
                "title": "Browsing Books",
                "items": [
                    "Use the search bar to find specific books.",
                    "Filter by genre or availability status.",
                    "Click 'View Details' to see complete book information.",
                    "Green 'Available' badges indicate books you can borrow."
                ]
            },
            {
                "title": "Managing Your Books",
                "items": [
                    "View your borrowed books in 'My Books' section.",
                    "Check due dates to avoid overdue fees.",
                    "Return books on time to maintain good standing.",
                    "View your complete borrowing history in the History tab."
                ]
            }
        ]

    # HELPER METHODS
    def _get_overdue_count(self):
        """Get count of overdue books"""
        if not self.db or not self.db.conn:
            return 0

        try:
            borrowed_books = self.get_borrowed_books()
            overdue_count = sum(1 for book in borrowed_books if book.get("status") == "Overdue")
            return overdue_count
        except:
            return 0

    def _get_history_count(self):
        """Get count of historical borrows"""
        if not self.db or not self.db.conn:
            return 0

        try:
            self.db.cursor.execute(
                "SELECT borrowed_count FROM users WHERE member_id = %s",
                (self.member_id,)
            )
            result = self.db.cursor.fetchone()
            return result['borrowed_count'] if result else 0
        except:
            return 0

    def _show_database_error(self):
        """Show database connection error"""
        if hasattr(self.current_window, 'show_message'):
            self.current_window.show_message(
                "Database Error",
                "Unable to connect to database. Please try again later.",
                "error"
            )
        else:
            print("Database connection error - no current window to show message")