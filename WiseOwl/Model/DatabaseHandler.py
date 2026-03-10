# Model/DatabaseHandler.py
import mysql.connector
from datetime import date, timedelta
import logging

# Database Configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''  # Set your MySQL password here
DB_NAME = 'PyCharm'

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseHandler:
    """Main database handler class"""

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.is_connected = False

    def connect(self):
        """Establishes a connection with MySQL database"""
        try:
            # First connect without database
            temp_conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD
            )
            temp_cursor = temp_conn.cursor()

            # Create database if it doesn't exist
            temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            temp_conn.database = DB_NAME

            # Now close temp connection and create real connection
            temp_cursor.close()
            temp_conn.close()

            # Connect to the database
            self.conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            self.cursor = self.conn.cursor(dictionary=True)  # Return results as dictionaries
            self.is_connected = True

            # Setup tables
            self._setup_tables()

            logger.info("✅ Connected to Database")
            return True

        except mysql.connector.Error as err:
            logger.error(f"❌ Failed to connect to database: {err}")
            self.is_connected = False
            return False

    def _setup_tables(self):
        """Creates tables if they don't exist"""
        try:
            # Create categories table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) UNIQUE NOT NULL
                )
            """)

            # Create users table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_name VARCHAR(100) NOT NULL,
                    member_id VARCHAR(50) UNIQUE NOT NULL,
                    category_id INT,
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    join_date DATE DEFAULT(CURRENT_DATE),
                    borrowed_count INT DEFAULT 0,
                    overdue_count INT DEFAULT 0,
                    FOREIGN KEY(category_id) REFERENCES categories(id) ON UPDATE CASCADE
                )
            """)

            # Create admin access code table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS adminacc_code (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    access_code VARCHAR(100) UNIQUE NOT NULL
                )
            """)

            # Create books table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    author VARCHAR(100) NOT NULL,
                    genre VARCHAR(50),
                    description TEXT,
                    total_copies INT DEFAULT 1,
                    available_copies INT DEFAULT 1,
                    location VARCHAR(50)
                )
            """)

            # Create borrow records table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS borrow_records (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    member_id VARCHAR(50),
                    book_id INT,
                    book_title VARCHAR(200),
                    borrow_date DATE,
                    due_date DATE,
                    return_date DATE,
                    condition_on_return VARCHAR(20),
                    status VARCHAR(20) DEFAULT 'Borrowed',
                    FOREIGN KEY(member_id) REFERENCES users(member_id) ON DELETE CASCADE,
                    FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE CASCADE
                )
            """)

            self.conn.commit()

            # Insert initial data
            self._insert_initial_data()

            logger.info("✅ Tables created successfully")
            return True

        except mysql.connector.Error as err:
            logger.error(f"❌ Failed to create tables: {err}")
            self.conn.rollback()
            return False

    def _insert_initial_data(self):
        """Insert initial data if tables are empty"""
        try:
            # Check if categories exist
            self.cursor.execute("SELECT COUNT(*) as count FROM categories")
            if self.cursor.fetchone()['count'] == 0:
                # Insert ONLY 2 categories
                self.cursor.execute("INSERT INTO categories (name) VALUES ('Library User')")
                self.cursor.execute("INSERT INTO categories (name) VALUES ('Library Admin')")

            # Check if admin codes exist
            self.cursor.execute("SELECT COUNT(*) as count FROM adminacc_code")
            if self.cursor.fetchone()['count'] == 0:
                admin_codes = ["ADmin5", "Admin45", "LibAD34"]
                for code in admin_codes:
                    self.cursor.execute("INSERT IGNORE INTO adminacc_code (access_code) VALUES (%s)", (code,))

            self.conn.commit()

        except mysql.connector.Error as err:
            logger.error(f"❌ Error inserting initial data: {err}")
            self.conn.rollback()

    def _ensure_librarian_columns(self):
        """Ensure the processed_by columns exist in borrow_records table"""

        def _ensure_librarian_columns(self):
            """Ensure the processed_by columns exist in borrow_records table"""
            try:
                # Check if processed_by column exists
                self.cursor.execute("""
                    SELECT COUNT(*) as count 
                    FROM information_schema.columns 
                    WHERE table_schema = %s 
                    AND table_name = 'borrow_records' 
                    AND column_name = 'processed_by'
                """, (DB_NAME,))

                if self.cursor.fetchone()['count'] == 0:
                    print("📝 Adding processed_by columns to borrow_records table...")

                    # Add the columns
                    self.cursor.execute("""
                        ALTER TABLE borrow_records 
                        ADD COLUMN processed_by VARCHAR(50) DEFAULT NULL,
                        ADD COLUMN processed_by_name VARCHAR(100) DEFAULT NULL
                    """)
                    self.conn.commit()
                    print("✅ Successfully added processed_by columns")
            except Exception as e:
                print(f"⚠️ Could not add librarian columns: {e}")

    # ========== USER/LOGIN METHODS ==========

    def verify_login(self, full_name, member_id):
        """Check if user exists and return their role"""
        try:
            query = """
                SELECT u.user_name, u.member_id, c.name as role
                FROM users u
                JOIN categories c ON u.category_id = c.id
                WHERE u.user_name = %s AND u.member_id = %s
            """
            self.cursor.execute(query, (full_name, member_id))
            result = self.cursor.fetchone()
            return result  # Returns dict: {'user_name': name, 'member_id': id, 'role': role}

        except mysql.connector.Error as err:
            logger.error(f"❌ Login verification failed: {err}")
            return None

    def verify_admin_code(self, access_code):
        """Check if admin code is valid"""
        try:
            query = "SELECT access_code FROM adminacc_code WHERE access_code = %s"
            self.cursor.execute(query, (access_code,))
            return self.cursor.fetchone() is not None

        except mysql.connector.Error as err:
            logger.error(f"❌ Admin code verification failed: {err}")
            return False

    # ========== BOOK METHODS ==========

    def get_all_books(self):
        """Get all books from database"""
        try:
            query = """
                SELECT id, title, author, genre, description, 
                       total_copies, available_copies, location
                FROM books
                ORDER BY title
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()

        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting all books: {err}")
            return []

    def get_all_books_detailed(self):
        """Get all books with complete details for catalog"""
        try:
            query = """
                SELECT id, title, author, genre, description, 
                       available_copies, location,
                       CASE 
                           WHEN available_copies > 0 THEN 'Available'
                           ELSE 'Borrowed'
                       END as status
                FROM books
                ORDER BY title
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()

        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting all books with details: {err}")
            return []

    def search_books(self, query):
        """Search books by title, author, or genre"""
        try:
            search_term = f"%{query}%"
            query_sql = """
                SELECT id, title, author, genre, description, 
                       total_copies, available_copies, location
                FROM books
                WHERE title LIKE %s
                   OR author LIKE %s
                   OR genre LIKE %s
                ORDER BY title
            """
            self.cursor.execute(query_sql, (search_term, search_term, search_term))
            return self.cursor.fetchall()

        except mysql.connector.Error as err:
            logger.error(f"❌ Error searching books: {err}")
            return []

    def search_books_detailed(self, query):
        """Search books by title or author with all details for UI"""
        try:
            search_term = f"%{query}%"
            query_sql = """
                SELECT id, title, author, genre, description, 
                       available_copies, location,
                       CASE 
                           WHEN available_copies > 0 THEN 'Available'
                           ELSE 'Borrowed'
                       END as status
                FROM books
                WHERE title LIKE %s
                   OR author LIKE %s
                   OR genre LIKE %s
                ORDER BY title
            """
            self.cursor.execute(query_sql, (search_term, search_term, search_term))
            return self.cursor.fetchall()

        except mysql.connector.Error as err:
            logger.error(f"❌ Error searching books with details: {err}")
            return []

    def get_book_by_id(self, book_id):
        """Get complete book details by ID"""
        try:
            query = """
                SELECT id, title, author, genre, description, 
                       total_copies, available_copies, location
                FROM books
                WHERE id = %s
            """
            self.cursor.execute(query, (book_id,))
            return self.cursor.fetchone()

        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting book by ID: {err}")
            return None

    def add_book(self, book_data):
        """Add new book to database"""
        try:
            query = """
                INSERT INTO books 
                (title, author, genre, description, total_copies, available_copies, location)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                book_data.get('title'),
                book_data.get('author'),
                book_data.get('genre', ''),
                book_data.get('description', ''),
                book_data.get('total_copies', 1),
                book_data.get('available_copies', book_data.get('total_copies', 1)),
                book_data.get('location', '')
            )

            self.cursor.execute(query, values)
            self.conn.commit()
            logger.info(f"✅ Book added: {book_data.get('title')}")
            return True, "Book added successfully"

        except mysql.connector.Error as err:
            logger.error(f"❌ Error adding book: {err}")
            self.conn.rollback()
            return False, f"Error adding book: {err}"

    def update_book(self, book_id, book_data):
        """Update existing book"""
        try:
            # Check if book exists
            self.cursor.execute("SELECT id FROM books WHERE id = %s", (book_id,))
            if not self.cursor.fetchone():
                return False, "Book not found"

            query = """
                UPDATE books 
                SET title = %s, 
                    author = %s, 
                    genre = %s, 
                    description = %s, 
                    total_copies = %s,
                    available_copies = %s,
                    location = %s
                WHERE id = %s
            """

            values = (
                book_data.get('title'),
                book_data.get('author'),
                book_data.get('genre', ''),
                book_data.get('description', ''),
                book_data.get('total_copies'),
                book_data.get('available_copies'),
                book_data.get('location', ''),
                book_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()
            logger.info(f"✅ Book updated: ID {book_id}")
            return True, "Book updated successfully"

        except mysql.connector.Error as err:
            logger.error(f"❌ Error updating book: {err}")
            self.conn.rollback()
            return False, f"Error updating book: {err}"

    def delete_book(self, book_id):
        """Delete book from database"""
        try:
            # Check if book exists
            self.cursor.execute("SELECT title FROM books WHERE id = %s", (book_id,))
            result = self.cursor.fetchone()
            if not result:
                return False, "Book not found"

            book_title = result['title']

            # Check if book is currently borrowed
            self.cursor.execute(
                "SELECT COUNT(*) as count FROM borrow_records WHERE book_id = %s AND status = 'Borrowed'",
                (book_id,)
            )
            borrowed_count = self.cursor.fetchone()['count']

            if borrowed_count > 0:
                return False, f"Cannot delete '{book_title}' - it is currently borrowed by {borrowed_count} member(s)"

            # Delete the book
            self.cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
            self.conn.commit()
            logger.info(f"✅ Book deleted: ID {book_id}")
            return True, f"Book '{book_title}' deleted successfully"

        except mysql.connector.Error as err:
            logger.error(f"❌ Error deleting book: {err}")
            self.conn.rollback()
            return False, f"Error deleting book: {err}"

    # ========== USER/MEMBER METHODS ==========

    def get_all_users(self):
        """Get all users from database with real-time overdue counts"""
        try:
            # First update overdue counts
            self.update_overdue_counts()

            query = """
                SELECT 
                    u.user_name, 
                    u.email, 
                    u.join_date, 
                    u.borrowed_count, 
                    u.overdue_count,
                    u.member_id,
                    (
                        SELECT COUNT(*) 
                        FROM borrow_records br 
                        WHERE br.member_id = u.member_id 
                        AND br.status = 'Borrowed'
                    ) as currently_borrowed
                FROM users u
                JOIN categories c ON u.category_id = c.id
                WHERE c.name = 'Library User'
                ORDER BY u.user_name
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting all users: {err}")
            return []

    def get_user_books(self, member_id):
        """Get all books borrowed by a user (for UserController)"""
        try:
            query = """
                SELECT 
                    br.book_title,
                    b.author,
                    br.due_date,
                    br.status
                FROM borrow_records br
                JOIN books b ON br.book_id = b.id
                WHERE br.member_id = %s 
                    AND br.status IN ('Borrowed', 'Overdue')
                ORDER BY br.due_date
            """
            self.cursor.execute(query, (member_id,))
            return self.cursor.fetchall()

        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting user books: {err}")
            return []

    def get_member_details(self, member_id):
        """Get complete member details by ID"""
        try:
            query = """
                SELECT user_name, member_id, email, phone, join_date, 
                       borrowed_count, overdue_count
                FROM users 
                WHERE member_id = %s
            """
            self.cursor.execute(query, (member_id,))
            result = self.cursor.fetchone()

            if result:
                return {
                    "name": result['user_name'],
                    "member_id": result['member_id'],
                    "email": result['email'],
                    "phone": result['phone'],
                    "join_date": str(result['join_date']),
                    "borrowed": result['borrowed_count'],
                    "overdue": result['overdue_count']
                }
            return None

        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting member details: {err}")
            return None

    # Add this method to DatabaseHandler.py (around line 300-320)

    def search_members(self, query):
        """Search members by name, email, or member_id"""
        try:
            search_term = f"%{query}%"
            query_sql = """
                SELECT u.user_name, u.email, u.join_date, u.borrowed_count, 
                       u.overdue_count, u.member_id
                FROM users u
                JOIN categories c ON u.category_id = c.id
                WHERE c.name = 'Library User'
                    AND (u.user_name LIKE %s 
                         OR u.email LIKE %s 
                         OR u.member_id LIKE %s)
                ORDER BY u.user_name
            """
            self.cursor.execute(query_sql, (search_term, search_term, search_term))
            return self.cursor.fetchall()

        except mysql.connector.Error as err:
            logger.error(f"❌ Error searching members: {err}")
            return []

    def add_member(self, member_data):
        """Add new member to database"""
        try:
            # Get Library User category ID
            self.cursor.execute("SELECT id FROM categories WHERE name = 'Library User'")
            category_result = self.cursor.fetchone()
            if not category_result:
                return False, "Library User category not found"
            category_id = category_result['id']

            # Check if member_id already exists
            self.cursor.execute("SELECT member_id FROM users WHERE member_id = %s", (member_data.get('member_id'),))
            if self.cursor.fetchone():
                return False, f"Member ID '{member_data.get('member_id')}' already exists"

            query = """
                INSERT INTO users 
                (user_name, member_id, category_id, email, phone, join_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                member_data.get('name'),
                member_data.get('member_id'),
                category_id,
                member_data.get('email', ''),
                member_data.get('phone', ''),
                date.today()
            )

            self.cursor.execute(query, values)
            self.conn.commit()
            logger.info(f"✅ Member added: {member_data.get('name')}")
            return True, "Member added successfully"

        except mysql.connector.Error as err:
            logger.error(f"❌ Error adding member: {err}")
            self.conn.rollback()
            return False, f"Error adding member: {err}"

    def update_member(self, member_id, member_data):
        """Update existing member"""
        try:
            # Check if member exists
            self.cursor.execute("SELECT member_id FROM users WHERE member_id = %s", (member_id,))
            if not self.cursor.fetchone():
                return False, "Member not found"

            query = """
                UPDATE users 
                SET user_name = %s, 
                    email = %s, 
                    phone = %s
                WHERE member_id = %s
            """

            values = (
                member_data.get('name'),
                member_data.get('email', ''),
                member_data.get('phone', ''),
                member_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()
            logger.info(f"✅ Member updated: {member_id}")
            return True, "Member updated successfully"

        except mysql.connector.Error as err:
            logger.error(f"❌ Error updating member: {err}")
            self.conn.rollback()
            return False, f"Error updating member: {err}"

    def delete_member(self, member_id):
        """Delete member from database"""
        try:
            # Check if member exists
            self.cursor.execute("SELECT user_name FROM users WHERE member_id = %s", (member_id,))
            result = self.cursor.fetchone()
            if not result:
                return False, "Member not found"

            user_name = result['user_name']

            # Check if member has borrowed books
            self.cursor.execute(
                "SELECT COUNT(*) as count FROM borrow_records WHERE member_id = %s AND status = 'Borrowed'",
                (member_id,)
            )
            borrowed_count = self.cursor.fetchone()['count']

            if borrowed_count > 0:
                return False, f"Cannot delete '{user_name}' - they have {borrowed_count} borrowed book(s)"

            # Delete the member
            self.cursor.execute("DELETE FROM users WHERE member_id = %s", (member_id,))
            self.conn.commit()
            logger.info(f"✅ Member deleted: {member_id}")
            return True, f"Member '{user_name}' deleted successfully"

        except mysql.connector.Error as err:
            logger.error(f"❌ Error deleting member: {err}")
            self.conn.rollback()
            return False, f"Error deleting member: {err}"



    # ========== TRANSACTION/REPORT METHODS ==========

    def get_transaction_history(self, limit=100, offset=0):
        """Get complete transaction history with real timestamps and librarian info"""
        try:
            query = """
                SELECT 
                    br.id as transaction_id,
                    br.member_id,
                    u.user_name as member_name,
                    br.book_id,
                    b.title as book_title,
                    b.author as book_author,
                    br.borrow_date,
                    br.due_date,
                    br.return_date,
                    br.condition_on_return,
                    br.status,
                    -- Use actual timestamps (since we only store dates, we'll use current time for demo)
                    -- In a real system, you'd have actual time fields
                    CASE 
                        WHEN br.status = 'Borrowed' THEN 'Checkout'
                        ELSE 'Return'
                    END as transaction_type,
                    -- Get librarian info
                    COALESCE(br.processed_by_name, 'System') as librarian_name,
                    COALESCE(br.processed_by, 'SYSTEM') as librarian_id,
                    -- Calculate overdue info
                    CASE 
                        WHEN br.status = 'Borrowed' AND br.due_date < CURDATE() 
                        THEN DATEDIFF(CURDATE(), br.due_date)
                        WHEN br.status = 'Returned' AND br.return_date > br.due_date
                        THEN DATEDIFF(br.return_date, br.due_date)
                        ELSE 0
                    END as days_overdue,
                    CASE 
                        WHEN br.status = 'Borrowed' AND br.due_date < CURDATE() 
                        THEN DATEDIFF(CURDATE(), br.due_date) * 50
                        WHEN br.status = 'Returned' AND br.return_date > br.due_date
                        THEN DATEDIFF(br.return_date, br.due_date) * 50
                        ELSE 0
                    END as overdue_fee
                FROM borrow_records br
                JOIN users u ON br.member_id = u.member_id
                JOIN books b ON br.book_id = b.id
                ORDER BY 
                    CASE 
                        WHEN br.status = 'Borrowed' THEN br.borrow_date
                        ELSE br.return_date
                    END DESC,
                    br.id DESC
                LIMIT %s OFFSET %s
            """
            self.cursor.execute(query, (limit, offset))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting transaction history: {err}")
            return []

    def get_transactions_by_date_range(self, start_date, end_date):
        """Get transactions within a date range"""
        try:
            query = """
                   SELECT 
                       br.id as transaction_id,
                       br.member_id,
                       u.user_name as member_name,
                       br.book_id,
                       b.title as book_title,
                       b.author as book_author,
                       br.borrow_date as checkout_date,
                       br.due_date,
                       br.return_date,
                       br.condition_on_return,
                       br.status,
                       DATE_FORMAT(br.borrow_date, '%h:%i %p') as checkout_time,
                       DATE_FORMAT(br.return_date, '%h:%i %p') as return_time,
                       DATEDIFF(br.return_date, br.borrow_date) as days_borrowed,
                       CASE 
                           WHEN br.return_date > br.due_date THEN 'Yes'
                           ELSE 'No'
                       END as was_overdue,
                       CASE 
                           WHEN br.return_date > br.due_date 
                           THEN DATEDIFF(br.return_date, br.due_date)
                           ELSE 0
                       END as overdue_days,
                       CASE 
                           WHEN br.return_date > br.due_date 
                           THEN DATEDIFF(br.return_date, br.due_date) * 50
                           ELSE 0
                       END as overdue_fee
                   FROM borrow_records br
                   JOIN users u ON br.member_id = u.member_id
                   JOIN books b ON br.book_id = b.id
                   WHERE br.borrow_date BETWEEN %s AND %s
                      OR br.return_date BETWEEN %s AND %s
                   ORDER BY br.borrow_date DESC
               """
            self.cursor.execute(query, (start_date, end_date, start_date, end_date))
            return self.cursor.fetchall()

        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting transactions by date: {err}")
            return []

    def get_transactions_by_member(self, member_id):
        """Get all transactions for a specific member"""
        try:
            query = """
                   SELECT 
                       br.id as transaction_id,
                       br.member_id,
                       u.user_name as member_name,
                       br.book_id,
                       b.title as book_title,
                       b.author as book_author,
                       br.borrow_date as checkout_date,
                       br.due_date,
                       br.return_date,
                       br.condition_on_return,
                       br.status,
                       DATE_FORMAT(br.borrow_date, '%h:%i %p') as checkout_time,
                       DATE_FORMAT(br.return_date, '%h:%i %p') as return_time,
                       DATEDIFF(br.return_date, br.borrow_date) as days_borrowed,
                       CASE 
                           WHEN br.return_date > br.due_date THEN 'Yes'
                           ELSE 'No'
                       END as was_overdue,
                       CASE 
                           WHEN br.return_date > br.due_date 
                           THEN DATEDIFF(br.return_date, br.due_date)
                           ELSE 0
                       END as overdue_days,
                       CASE 
                           WHEN br.return_date > br.due_date 
                           THEN DATEDIFF(br.return_date, br.due_date) * 50
                           ELSE 0
                       END as overdue_fee
                   FROM borrow_records br
                   JOIN users u ON br.member_id = u.member_id
                   JOIN books b ON br.book_id = b.id
                   WHERE br.member_id = %s
                   ORDER BY br.borrow_date DESC
               """
            self.cursor.execute(query, (member_id,))
            return self.cursor.fetchall()

        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting member transactions: {err}")
            return []

    def get_transactions_by_librarian(self, librarian_id):
        """Get all transactions processed by a specific librarian"""
        # You'll need to add a processed_by column to your borrow_records table
        try:
            # First, check if processed_by column exists
            self.cursor.execute("""
                   SELECT COUNT(*) as count 
                   FROM information_schema.columns 
                   WHERE table_name = 'borrow_records' 
                   AND column_name = 'processed_by'
               """)
            if self.cursor.fetchone()['count'] == 0:
                # Add the column if it doesn't exist
                self.cursor.execute("""
                       ALTER TABLE borrow_records 
                       ADD COLUMN processed_by VARCHAR(50),
                       ADD COLUMN processed_by_name VARCHAR(100)
                   """)
                self.conn.commit()

            query = """
                   SELECT 
                       br.id as transaction_id,
                       br.member_id,
                       u.user_name as member_name,
                       br.book_id,
                       b.title as book_title,
                       b.author as book_author,
                       br.borrow_date as checkout_date,
                       br.due_date,
                       br.return_date,
                       br.condition_on_return,
                       br.status,
                       br.processed_by as librarian_id,
                       br.processed_by_name as librarian_name,
                       DATE_FORMAT(br.borrow_date, '%h:%i %p') as checkout_time,
                       DATE_FORMAT(br.return_date, '%h:%i %p') as return_time
                   FROM borrow_records br
                   JOIN users u ON br.member_id = u.member_id
                   JOIN books b ON br.book_id = b.id
                   WHERE br.processed_by = %s
                   ORDER BY br.borrow_date DESC
               """
            self.cursor.execute(query, (librarian_id,))
            return self.cursor.fetchall()

        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting librarian transactions: {err}")
            return []

    def get_detailed_circulation_report(self, report_type="all"):
        """Get detailed circulation data with real timestamps and librarian info"""
        try:
            # First ensure processed_by columns exist
            self._ensure_librarian_columns()

            if report_type == "checkouts_only":
                query = """
                    SELECT 
                        'Checkout' as transaction_type,
                        br.id as transaction_id,
                        br.member_id,
                        u.user_name as member_name,
                        br.book_id,
                        b.title as book_title,
                        b.author as book_author,
                        br.borrow_date as transaction_date,
                        br.due_date,
                        NULL as return_date,
                        'Borrowed' as status,
                        -- Get librarian info with fallback
                        COALESCE(br.processed_by_name, 
                                (SELECT user_name FROM users WHERE member_id = br.processed_by),
                                'System') as librarian_name,
                        COALESCE(br.processed_by, 'SYSTEM') as librarian_id,
                        -- Calculate overdue fee for active borrows
                        CASE 
                            WHEN br.due_date < CURDATE() 
                            THEN DATEDIFF(CURDATE(), br.due_date) * 50
                            ELSE 0
                        END as overdue_fee,
                        -- Days overdue
                        CASE 
                            WHEN br.due_date < CURDATE() 
                            THEN DATEDIFF(CURDATE(), br.due_date)
                            ELSE 0
                        END as days_overdue
                    FROM borrow_records br
                    JOIN users u ON br.member_id = u.member_id
                    JOIN books b ON br.book_id = b.id
                    WHERE br.status = 'Borrowed'
                    ORDER BY br.borrow_date DESC
                """
            elif report_type == "returns_only":
                query = """
                    SELECT 
                        'Return' as transaction_type,
                        br.id as transaction_id,
                        br.member_id,
                        u.user_name as member_name,
                        br.book_id,
                        b.title as book_title,
                        b.author as book_author,
                        br.return_date as transaction_date,
                        br.borrow_date,
                        br.return_date,
                        'Returned' as status,
                        -- Get librarian info with fallback
                        COALESCE(br.processed_by_name,
                                (SELECT user_name FROM users WHERE member_id = br.processed_by),
                                'System') as librarian_name,
                        COALESCE(br.processed_by, 'SYSTEM') as librarian_id,
                        -- Calculate overdue fee for returns
                        CASE 
                            WHEN br.return_date > br.due_date 
                            THEN DATEDIFF(br.return_date, br.due_date) * 50
                            ELSE 0
                        END as overdue_fee,
                        -- Days overdue
                        CASE 
                            WHEN br.return_date > br.due_date 
                            THEN DATEDIFF(br.return_date, br.due_date)
                            ELSE 0
                        END as days_overdue
                    FROM borrow_records br
                    JOIN users u ON br.member_id = u.member_id
                    JOIN books b ON br.book_id = b.id
                    WHERE br.status = 'Returned'
                    ORDER BY br.return_date DESC
                """
            else:  # all transactions
                query = """
                    SELECT 
                        CASE 
                            WHEN br.status = 'Borrowed' THEN 'Checkout'
                            ELSE 'Return'
                        END as transaction_type,
                        br.id as transaction_id,
                        br.member_id,
                        u.user_name as member_name,
                        br.book_id,
                        b.title as book_title,
                        b.author as book_author,
                        CASE 
                            WHEN br.status = 'Borrowed' THEN br.borrow_date
                            ELSE br.return_date
                        END as transaction_date,
                        br.borrow_date,
                        br.due_date,
                        br.return_date,
                        br.status,
                        br.condition_on_return,
                        -- Get librarian info with fallback to actual user names
                        COALESCE(br.processed_by_name,
                                (SELECT user_name FROM users WHERE member_id = br.processed_by),
                                'System') as librarian_name,
                        COALESCE(br.processed_by, 'SYSTEM') as librarian_id,
                        -- Calculate overdue fee
                        CASE 
                            WHEN br.status = 'Borrowed' AND br.due_date < CURDATE() 
                            THEN DATEDIFF(CURDATE(), br.due_date) * 50
                            WHEN br.status = 'Returned' AND br.return_date > br.due_date
                            THEN DATEDIFF(br.return_date, br.due_date) * 50
                            ELSE 0
                        END as overdue_fee,
                        -- Days overdue
                        CASE 
                            WHEN br.status = 'Borrowed' AND br.due_date < CURDATE() 
                            THEN DATEDIFF(CURDATE(), br.due_date)
                            WHEN br.status = 'Returned' AND br.return_date > br.due_date
                            THEN DATEDIFF(br.return_date, br.due_date)
                            ELSE 0
                        END as days_overdue,
                        -- Member borrowing stats
                        u.borrowed_count as member_total_borrowed,
                        u.overdue_count as member_total_overdue
                    FROM borrow_records br
                    JOIN users u ON br.member_id = u.member_id
                    JOIN books b ON br.book_id = b.id
                    ORDER BY transaction_date DESC, br.id DESC
                """

            self.cursor.execute(query)
            results = self.cursor.fetchall()
            print(f"📊 Found {len(results)} transactions for report")

            # Debug: Print first few transactions to check librarian names
            if results and len(results) > 0:
                print("🔍 Sample transaction librarian names:")
                for i, trans in enumerate(results[:3]):
                    print(f"   Transaction {i + 1}: Librarian = {trans.get('librarian_name', 'N/A')}")

            return results
        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting circulation report: {err}")
            return []

    def get_circulation_summary(self):
        """Get summary statistics for circulation"""
        try:
            summary = {}

            # Total transactions
            self.cursor.execute("SELECT COUNT(*) as total FROM borrow_records")
            summary['total_transactions'] = self.cursor.fetchone()['total']

            # Today's transactions
            self.cursor.execute("""
                   SELECT 
                       COUNT(*) as today_total,
                       SUM(CASE WHEN status = 'Borrowed' THEN 1 ELSE 0 END) as today_checkouts,
                       SUM(CASE WHEN status = 'Returned' THEN 1 ELSE 0 END) as today_returns
                   FROM borrow_records 
                   WHERE borrow_date = CURDATE() OR return_date = CURDATE()
               """)
            today_stats = self.cursor.fetchone()
            summary['today_transactions'] = today_stats['today_total'] or 0
            summary['today_checkouts'] = today_stats['today_checkouts'] or 0
            summary['today_returns'] = today_stats['today_returns'] or 0

            # This week's transactions
            self.cursor.execute("""
                   SELECT COUNT(*) as week_total
                   FROM borrow_records 
                   WHERE borrow_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                      OR return_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
               """)
            summary['week_transactions'] = self.cursor.fetchone()['week_total'] or 0

            # This month's transactions
            self.cursor.execute("""
                   SELECT COUNT(*) as month_total
                   FROM borrow_records 
                   WHERE MONTH(borrow_date) = MONTH(CURDATE()) 
                      OR MONTH(return_date) = MONTH(CURDATE())
               """)
            summary['month_transactions'] = self.cursor.fetchone()['month_total'] or 0

            # Average daily transactions
            self.cursor.execute("""
                   SELECT 
                       COUNT(*) / DATEDIFF(MAX(borrow_date), MIN(borrow_date)) as avg_daily
                   FROM borrow_records
               """)
            result = self.cursor.fetchone()
            summary['avg_daily_transactions'] = round(result['avg_daily'] or 0, 1)

            # Most active members
            self.cursor.execute("""
                   SELECT 
                       u.user_name,
                       u.member_id,
                       COUNT(*) as transaction_count
                   FROM borrow_records br
                   JOIN users u ON br.member_id = u.member_id
                   GROUP BY u.user_name, u.member_id
                   ORDER BY transaction_count DESC
                   LIMIT 5
               """)
            summary['top_members'] = self.cursor.fetchall()

            # Most borrowed books
            self.cursor.execute("""
                   SELECT 
                       b.title,
                       b.author,
                       COUNT(*) as borrow_count
                   FROM borrow_records br
                   JOIN books b ON br.book_id = b.id
                   GROUP BY b.title, b.author
                   ORDER BY borrow_count DESC
                   LIMIT 5
               """)
            summary['top_books'] = self.cursor.fetchall()

            return summary

        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting circulation summary: {err}")
            return {}

    # ========== CIRCULATION METHODS ==========

    def process_checkout(self, member_id, book_id, librarian_id=None, librarian_name=None):
        """Process book checkout - Now with librarian info"""
        try:
            # FIRST CHECK: Does member have overdue books?
            if self.has_overdue_books(member_id):
                # Get the overdue books details for the message
                overdue_query = """
                    SELECT book_title, due_date, DATEDIFF(CURDATE(), due_date) as days
                    FROM borrow_records
                    WHERE member_id = %s 
                        AND status = 'Borrowed'
                        AND due_date < CURDATE()
                    ORDER BY due_date
                """
                self.cursor.execute(overdue_query, (member_id,))
                overdue_books = self.cursor.fetchall()

                # Create detailed message
                book_list = "\n".join([f"  • {b['book_title']} (Due: {b['due_date']}, {b['days']} days overdue)"
                                       for b in overdue_books])

                error_message = (
                    f"Cannot borrow books. Member has {len(overdue_books)} overdue book(s):\n\n"
                    f"{book_list}\n\n"
                    f"Please return overdue books before borrowing new ones."
                )

                return False, error_message, None

            # Check if member exists
            self.cursor.execute("SELECT user_name FROM users WHERE member_id = %s", (member_id,))
            member_result = self.cursor.fetchone()
            if not member_result:
                return False, f"Member ID {member_id} not found", None

            member_name = member_result['user_name']

            # Check if book exists and is available
            self.cursor.execute("""
                SELECT id, title, author, available_copies 
                FROM books 
                WHERE id = %s
            """, (book_id,))
            book_result = self.cursor.fetchone()

            if not book_result:
                return False, f"Book ID {book_id} not found", None

            title = book_result['title']
            author = book_result['author']
            available = book_result['available_copies']

            if available <= 0:
                return False, f"Book '{title}' is not available", None

            # Update book availability
            self.cursor.execute("""
                UPDATE books
                SET available_copies = available_copies - 1
                WHERE id = %s
            """, (book_id,))

            # Create borrow record
            borrow_date = date.today()
            due_date = borrow_date + timedelta(days=3)

            # Check if processed_by column exists
            self.cursor.execute("""
                SELECT COUNT(*) as count 
                FROM information_schema.columns 
                WHERE table_name = 'borrow_records' 
                AND column_name = 'processed_by'
            """)
            if self.cursor.fetchone()['count'] == 0:
                # Add the columns if they don't exist
                self.cursor.execute("""
                    ALTER TABLE borrow_records 
                    ADD COLUMN processed_by VARCHAR(50),
                    ADD COLUMN processed_by_name VARCHAR(100)
                """)
                self.conn.commit()

            if librarian_id and librarian_name:
                self.cursor.execute("""
                    INSERT INTO borrow_records
                    (member_id, book_id, book_title, borrow_date, due_date, status, processed_by, processed_by_name)
                    VALUES (%s, %s, %s, %s, %s, 'Borrowed', %s, %s)
                """, (member_id, book_id, title, borrow_date, due_date, librarian_id, librarian_name))
            else:
                self.cursor.execute("""
                    INSERT INTO borrow_records
                    (member_id, book_id, book_title, borrow_date, due_date, status)
                    VALUES (%s, %s, %s, %s, %s, 'Borrowed')
                """, (member_id, book_id, title, borrow_date, due_date))

            # Update user's borrowed count
            self.cursor.execute("""
                UPDATE users
                SET borrowed_count = borrowed_count + 1
                WHERE member_id = %s
            """, (member_id,))

            self.conn.commit()
            logger.info(f"✅ Book {book_id} checked out to {member_id}")

            # Format success message
            success_message = f"Book '{title}' checked out to {member_name}. Due on {due_date.strftime('%b %d, %Y')}"

            # Return receipt data along with success
            receipt_data = {
                'transaction_id': f"TX-{borrow_date.strftime('%Y%m%d')}-{book_id}-{member_id}",
                'member_name': member_name,
                'member_id': member_id,
                'book_title': title,
                'book_id': book_id,
                'book_author': author,
                'checkout_date': borrow_date.strftime("%b %d, %Y"),
                'due_date': due_date.strftime("%b %d, %Y"),
                'librarian_name': librarian_name,
                'librarian_id': librarian_id
            }

            return True, success_message, receipt_data

        except mysql.connector.Error as err:
            logger.error(f"❌ Error processing checkout: {err}")
            self.conn.rollback()
            return False, "Failed to process checkout", None

    def process_checkin(self, member_id, book_id, condition, librarian_id=None, librarian_name=None):
        """Process book checkin - Now with librarian info"""
        try:
            # Find the borrow record for this book AND member
            self.cursor.execute("""
                SELECT id, member_id, book_title
                FROM borrow_records
                WHERE book_id = %s
                    AND member_id = %s
                    AND status = 'Borrowed'
                ORDER BY borrow_date DESC LIMIT 1
            """, (book_id, member_id))

            result = self.cursor.fetchone()
            if not result:
                return False, f"No active borrow record found for book ID {book_id} by member {member_id}"

            record_id = result['id']
            title = result['book_title']
            return_date = date.today()

            # Update borrow record with librarian info if provided
            if librarian_id and librarian_name:
                self.cursor.execute("""
                    UPDATE borrow_records
                    SET return_date = %s,
                        condition_on_return = %s,
                        status = 'Returned',
                        processed_by = %s,
                        processed_by_name = %s
                    WHERE id = %s
                """, (return_date, condition, librarian_id, librarian_name, record_id))
            else:
                self.cursor.execute("""
                    UPDATE borrow_records
                    SET return_date = %s,
                        condition_on_return = %s,
                        status = 'Returned'
                    WHERE id = %s
                """, (return_date, condition, record_id))

            # Update book availability
            self.cursor.execute("""
                UPDATE books
                SET available_copies = available_copies + 1
                WHERE id = %s
            """, (book_id,))

            self.conn.commit()
            logger.info(f"✅ Book {book_id} checked in by {member_id}")
            return True, f"Book '{title}' checked in. Condition: {condition}"

        except mysql.connector.Error as err:
            logger.error(f"❌ Error processing checkin: {err}")
            self.conn.rollback()
            return False, "Failed to process checkin"

    def get_borrow_record(self, member_id, book_id):
        """Get active borrow record for a member and book"""
        try:
            query = """
                SELECT id, member_id, book_id, book_title, borrow_date, due_date, status
                FROM borrow_records
                WHERE member_id = %s 
                    AND book_id = %s 
                    AND status = 'Borrowed'
                ORDER BY borrow_date DESC
                LIMIT 1
            """
            self.cursor.execute(query, (member_id, book_id))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting borrow record: {err}")
            return None

    # ========== RECEIPT DATA METHODS ==========

    def get_book_details(self, book_id):
        """Get detailed book information by ID"""
        try:
            query = """
                SELECT id, title, author, genre, description, 
                       total_copies, available_copies, location
                FROM books
                WHERE id = %s
            """
            self.cursor.execute(query, (book_id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting book details: {err}")
            return None

    def get_member_details(self, member_id):
        """Get complete member details by ID"""
        try:
            query = """
                SELECT user_name, member_id, email, phone, join_date, 
                       borrowed_count, overdue_count
                FROM users 
                WHERE member_id = %s
            """
            self.cursor.execute(query, (member_id,))
            result = self.cursor.fetchone()

            if result:
                return {
                    "user_name": result['user_name'],
                    "member_id": result['member_id'],
                    "email": result['email'],
                    "phone": result['phone'],
                    "join_date": str(result['join_date']),
                    "borrowed": result['borrowed_count'],
                    "overdue": result['overdue_count']
                }
            return None
        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting member details: {err}")
            return None

    def get_latest_transaction(self, member_id, book_id):
        """Get the latest transaction for a member/book combination"""
        try:
            query = """
                SELECT id, member_id, book_id, book_title, borrow_date, due_date, status
                FROM borrow_records
                WHERE member_id = %s AND book_id = %s
                ORDER BY borrow_date DESC
                LIMIT 1
            """
            self.cursor.execute(query, (member_id, book_id))
            return self.cursor.fetchone()
        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting latest transaction: {err}")
            return None

    # ========== STATISTICS METHODS ==========

    def get_library_stats(self):
        """Get library statistics"""
        try:
            stats = {}

            # Total books (count of unique books)
            self.cursor.execute("SELECT COUNT(*) as total FROM books")
            stats["total_books"] = self.cursor.fetchone()['total']

            # Available copies (sum of available_copies)
            self.cursor.execute("SELECT SUM(available_copies) as available FROM books")
            result = self.cursor.fetchone()
            stats["available_books"] = result['available'] if result['available'] else 0

            # Total copies (sum of total_copies)
            self.cursor.execute("SELECT SUM(total_copies) as total FROM books")
            total_copies_result = self.cursor.fetchone()
            total_copies = total_copies_result['total'] if total_copies_result['total'] else 0

            # Borrowed books = total_copies - available_copies
            stats["borrowed_books"] = total_copies - stats["available_books"]

            # Total members (only Library Users, not admins)
            self.cursor.execute("""
                SELECT COUNT(*) as total 
                FROM users u
                JOIN categories c ON u.category_id = c.id
                WHERE c.name = 'Library User'
            """)
            stats["total_members"] = self.cursor.fetchone()['total']

            print(f"📊 Library Stats: {stats}")  # Debug print
            return stats

        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting library stats: {err}")
            return {"total_books": 0, "available_books": 0, "borrowed_books": 0, "total_members": 0}

    def get_overdue_books(self):
        """Get list of overdue books with proper formatting"""
        try:
            query = """
                SELECT 
                    br.book_title as title,
                    u.user_name as borrower,
                    DATEDIFF(CURDATE(), br.due_date) as days_overdue,
                    br.due_date,
                    u.member_id
                FROM borrow_records br
                JOIN users u ON br.member_id = u.member_id
                WHERE br.status = 'Borrowed' 
                    AND br.due_date < CURDATE()
                ORDER BY days_overdue DESC
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            print(f"\n📊 OVERDUE BOOKS FOUND: {len(results)}")
            for book in results:
                print(f"   - {book['title']} borrowed by {book['borrower']} ({book['days_overdue']} days overdue)")

            return results

        except mysql.connector.Error as err:
            logger.error(f"❌ Error getting overdue books: {err}")
            return []

    def update_overdue_counts(self):
        """Update the overdue_count field for all users based on current overdue books"""
        try:
            # First, reset all overdue counts
            self.cursor.execute("UPDATE users SET overdue_count = 0")

            # Then count overdue books per user and update
            query = """
                  UPDATE users u
                  SET u.overdue_count = (
                      SELECT COUNT(*)
                      FROM borrow_records br
                      WHERE br.member_id = u.member_id
                          AND br.status = 'Borrowed'
                          AND br.due_date < CURDATE()
                  )
              """
            self.cursor.execute(query)
            self.conn.commit()

            print("✅ Overdue counts updated successfully")
            return True
        except mysql.connector.Error as err:
            logger.error(f"❌ Error updating overdue counts: {err}")
            return False
    def has_overdue_books(self, member_id):
        """Check if a member has any overdue books"""
        try:
            query = """
                SELECT COUNT(*) as overdue_count
                FROM borrow_records
                WHERE member_id = %s 
                    AND status = 'Borrowed'
                    AND due_date < CURDATE()
            """
            self.cursor.execute(query, (member_id,))
            result = self.cursor.fetchone()

            overdue_count = result['overdue_count'] if result else 0
            return overdue_count > 0

        except mysql.connector.Error as err:
            logger.error(f"❌ Error checking overdue books: {err}")
            return False

    # ========== UTILITY METHODS ==========

    def close(self):
        """Close database connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            self.is_connected = False
            logger.info("✅ Database connection closed")
        except mysql.connector.Error as err:
            logger.error(f"❌ Error closing database: {err}")

    def is_connected(self):
        """Check if database is connected"""
        return self.is_connected