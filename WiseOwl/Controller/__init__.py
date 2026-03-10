# Controller/__init__.py
from .Authentification import AuthController
from .UserController import UserController
from .Admin import AdminController

__all__ = ['AuthController', 'UserController', 'AdminController']