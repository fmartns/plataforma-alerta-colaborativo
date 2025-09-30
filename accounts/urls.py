from django.urls import path
from .views import (
    UserCreateAPIView,
    UserProfileAPIView,
    ProfileUpdateAPIView,
    ProfileListAPIView,
    UserStatsAPIView,
    check_cpf_availability,
    list_neighborhoods,
    profile_view,
    check_cpf_legacy,
)
from .views.validation import validate_phone, validate_cep
from .views.admin import InactiveProfilesAPIView
from .views.legacy import user_profile_json

app_name = "accounts"

urlpatterns = [
    path("profile/", profile_view, name="profile"),
    path("profile/json/", user_profile_json, name="profile_json"),
    path("register/", UserCreateAPIView.as_view(), name="api_register"),
    path("me/", UserProfileAPIView.as_view(), name="api_user_profile"),
    path("me/profile/", ProfileUpdateAPIView.as_view(), name="api_profile_update"),
    path("profiles/", ProfileListAPIView.as_view(), name="api_profiles_list"),
    path(
        "profiles/inactive/",
        InactiveProfilesAPIView.as_view(),
        name="api_inactive_profiles",
    ),
    path("stats/", UserStatsAPIView.as_view(), name="api_user_stats"),
    path("validate/cpf/", check_cpf_availability, name="api_check_cpf"),
    path("validate/phone/", validate_phone, name="api_validate_phone"),
    path("validate/cep/", validate_cep, name="api_validate_cep"),
    path("neighborhoods/", list_neighborhoods, name="api_neighborhoods"),
    path("check-cpf/", check_cpf_legacy, name="check_cpf_legacy"),
]
