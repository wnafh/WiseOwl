# Model/__init__.py
from .User import User
from .Book import Book
from .Borrow import Borrow
from .DatabaseHandler import DatabaseHandler

__all__ = ['User', 'Book', 'Borrow', 'DatabaseHandler']