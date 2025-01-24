"""Expose accounts application configuration."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Accounts application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "webapp.accounts"
