"""Expose tasktrack application configuration."""

from django.apps import AppConfig


class TasktrackConfig(AppConfig):
    """Tasktrack application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "webapp.tasktrack"
