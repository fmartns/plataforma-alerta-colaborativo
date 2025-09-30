"""
Views modulares para o app accounts
"""

from .auth import UserCreateAPIView
from .profile import UserProfileAPIView, ProfileUpdateAPIView
from .admin import ProfileListAPIView, UserStatsAPIView, InactiveProfilesAPIView
from .validation import (
    check_cpf_availability,
    list_neighborhoods,
    validate_phone,
    validate_cep,
)
from .legacy import (
    profile_view,
    check_cpf_availability as check_cpf_legacy,
    user_profile_json,
)

__all__ = [
    "UserCreateAPIView",
    "UserProfileAPIView",
    "ProfileUpdateAPIView",
    "ProfileListAPIView",
    "UserStatsAPIView",
    "InactiveProfilesAPIView",
    "check_cpf_availability",
    "list_neighborhoods",
    "validate_phone",
    "validate_cep",
    "profile_view",
    "check_cpf_legacy",
    "user_profile_json",
]
