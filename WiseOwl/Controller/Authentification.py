# Controller/Authentification.py
import sys
from Model.DatabaseHandler import DatabaseHandler

class AuthController:
    def __init__(self):
        self.current_window = None
        self.user_data = {}
        self.admin_controller = None
        self.user_controller = None

        # Initialize database
        self.db = DatabaseHandler()
        self.db.connect()

    def set_application(self, app):
        """Set the QApplication instance"""
        self.app = app

    def start(self):
        """Start the application - called from main.py"""
        self.show_login_view()

    def show_login_view(self):
        # Import inside method to avoid circular imports
        from View.Log import LoginView

        if self.current_window:
            self._close_window(self.current_window)

        login_view = LoginView()
        login_view.login_success_callback = self.handle_login_success
        login_view.login_failed_callback = self.handle_login_failed
        login_view.show()
        self.current_window = login_view

    def handle_login_success(self, user_name, member_id):
        """Handle successful login - IMPROVED"""
        if self.db.conn:
            result = self.db.verify_login(user_name, member_id)

            if result:
                # Get user data from database
                name = result['user_name']
                actual_member_id = result['member_id']
                role = result['role']

                print(f"\n✅ LOGIN SUCCESS:")
                print(f"   User: {name}")
                print(f"   Member ID: {actual_member_id}")
                print(f"   Role: {role}")

                self.user_data = {
                    'name': name,
                    'member_id': actual_member_id,
                    'role': role
                }

                # **IMPROVED: Auto-route based on role**
                if role == "Library Admin":
                    print("   → Redirecting to Admin Verification...")
                    self.show_admin_verification()
                else:
                    print("   → Redirecting to User Dashboard...")
                    self.start_user_interface()
            else:
                # Delegate UI error to view
                self._call_view_method('show_error', "Invalid credentials. Please try again.")

    def handle_login_failed(self):
        """Handle login failure """
        # Delegate UI to view
        self._call_view_method('show_message', "Login Failed", "Please check your credentials and try again.", "error")

    def handle_logout(self):
        """Handle logout -"""
        # Clean up controllers
        if self.user_controller:
            self._close_controller(self.user_controller)
            self.user_controller = None

        if self.admin_controller:
            self._close_controller(self.admin_controller)
            self.admin_controller = None

        # Clear user data
        self.user_data = {}

        # Show login view
        self.show_login_view()

    def show_admin_verification(self):
        """Show admin verification screen - Only for admin roles"""
        from View.Admin import AdminVerificationView

        if self.current_window:
            self._close_window(self.current_window)

        verification_view = AdminVerificationView(
            self.user_data['name'],
            self.user_data['member_id'],
            'Library Admin'
        )

        verification_view.verify_callback = self.handle_admin_verification
        verification_view.back_callback = self.show_login_view

        verification_view.show()
        self.current_window = verification_view

    def handle_admin_verification(self, access_code):
        """Handle admin code verification"""
        is_valid = self.db.verify_admin_code(access_code)

        if is_valid:
            print("✅ Admin verification successful!")
            print(f"   → Starting Admin Interface for {self.user_data['name']}")
            self.start_admin_interface()
        else:
            # Delegate UI error to view
            self._call_view_method('show_message', "Invalid Code", "Please enter a valid admin access code", "error")

            # Clear input if view supports it
            if hasattr(self.current_window, 'clear_code_input'):
                self.current_window.clear_code_input()

    def start_admin_interface(self):
        """Start admin interface"""
        from Controller.Admin import AdminController

        # Store reference
        verification_window = self.current_window
        self.current_window = None

        # Create AdminController
        self.admin_controller = AdminController(
            self.user_data['name'],
            self.user_data['member_id'],
            self.user_data['role']
        )

        # Set logout callback
        self.admin_controller.logout_callback = self.handle_logout

        # Show admin dashboard
        self.admin_controller.show_dashboard()

        # Close verification window
        if verification_window:
            self._close_window(verification_window)

    def start_user_interface(self):
        """Start user interface"""
        from Controller.UserController import UserController

        # Create UserController
        self.user_controller = UserController(
            self.user_data['name'],
            self.user_data['member_id'],
            self.user_data['role'],
            self.db
        )

        # Set logout callback
        self.user_controller.logout_callback = self.handle_logout

        # Show user dashboard
        self.user_controller.show_my_books()

        # Close the current window
        if self.current_window:
            self._close_window(self.current_window)
            self.current_window = None

    # HELPER METHODS
    def _close_window(self, window):
        """Safely close a window"""
        try:
            window.close()
        except:
            pass

    def _close_controller(self, controller):
        """Safely close a controller"""
        try:
            if hasattr(controller, 'current_view') and controller.current_view:
                controller.current_view.close()
            elif hasattr(controller, 'current_window') and controller.current_window:
                controller.current_window.close()
        except:
            pass

    def _call_view_method(self, method_name, *args, **kwargs):
        """Call a method on the current view if it exists"""
        if self.current_window and hasattr(self.current_window, method_name):
            method = getattr(self.current_window, method_name)
            method(*args, **kwargs)