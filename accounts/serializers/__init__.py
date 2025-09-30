"""
Serializers modulares para o app accounts
"""

from .auth import CustomTokenObtainPairSerializer
from .user import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from .profile import (
    ProfileSerializer,
    ProfileUpdateSerializer,
    ProfileListSerializer,
    ProfileStatsSerializer,
)

__all__ = [
    "CustomTokenObtainPairSerializer",
    "UserSerializer",
    "UserCreateSerializer",
    "UserUpdateSerializer",
    "ProfileSerializer",
    "ProfileUpdateSerializer",
    "ProfileListSerializer",
    "ProfileStatsSerializer",
]
