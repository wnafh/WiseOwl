# main.py
import sys
from PyQt6.QtWidgets import QApplication
from Controller.Authentification import AuthController


def main():
    """Main entry point for the application"""
    # Create QApplication
    app = QApplication(sys.argv)

    # Create controller
    controller = AuthController()
    controller.set_application(app)

    # Start the application
    controller.start()

    # Execute the application
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())