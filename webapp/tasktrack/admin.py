"""Admin panel for the tasktrack application."""

from typing import Any

from django import forms
from django.contrib import admin
from django.http import HttpRequest
from django.utils import timezone
from django_select2.forms import Select2Widget

from webapp.tasktrack.models import Priority, Status, Task


class TaskAdminForm(forms.ModelForm):
    """Enable Select2 in admin."""

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "assigned_to": Select2Widget,
        }


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    """Custom admin class for priority model."""

    list_display = (
        "name",
        "description",
        "created_at",
    )

    list_filter = ("name",)

    search_fields = ("name",)
    ordering = ("-pk",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Custom admin class for status model."""

    list_display = (
        "name",
        "description",
        "created_at",
    )

    list_filter = ("name",)

    search_fields = ("name",)
    ordering = ("-pk",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Custom admin class for task model."""

    form = TaskAdminForm

    list_display = (
        "title",
        "due_date",
        "priority",
        "status",
        "assigned_to",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "updated_by",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "priority__name",
        "status__name",
    )

    search_fields = (
        "title",
        "assigned_to__first_name",
        "assigned_to__last_name",
        "assigned_to__email",
        "created_by__first_name",
        "created_by__last_name",
        "created_by__email",
        "updated_by__first_name",
        "updated_by__last_name",
        "updated_by__email",
    )
    ordering = ("-pk",)

    def save_model(
        self, request: HttpRequest, obj: Any, form: Any, change: bool
    ) -> None:
        """Save model method."""

        obj.updated_by = request.user
        obj.updated_at = timezone.now()
        obj.save()
