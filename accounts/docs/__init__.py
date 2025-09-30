"""
Documentação Swagger/OpenAPI modular do app accounts
"""

from . import auth
from . import profile
from . import admin
from . import validation
from . import jwt

__all__ = [
    "auth",
    "profile",
    "admin",
    "validation",
    "jwt",
]
