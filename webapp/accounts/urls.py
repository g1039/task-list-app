"""Expose the application url config."""

from django.urls import path

from webapp.accounts.views import (
    login_view,
    logout_view,
    password_reset_complete_view,
    password_reset_done_view,
    profile_detail_view,
    register_view,
    user_password_change_done_view,
    user_password_change_view,
    user_password_reset_confirm_view,
    user_password_reset_view,
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("forgot-password/", user_password_reset_view, name="forgot_password"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        user_password_reset_confirm_view,
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        password_reset_complete_view,
        name="password_reset_complete",
    ),
    path("password-reset-done/", password_reset_done_view, name="password_reset_done"),
    path("password-change/", user_password_change_view, name="password_change"),
    path(
        "accounts/password-change-done/",
        user_password_change_done_view,
        name="password_change_done",
    ),
    path("profile/", profile_detail_view, name="profile-detail"),
    path("logout/", logout_view, name="logout"),
]
