"""Database models for the tasktrack application."""

from typing import Any, Optional

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from webapp.accounts.models import CustomUser
from webapp.tasktrack.enums import PriorityLevel, StatusType
from webapp.tasktrack.managers import PriorityManager, StatusManager, TaskManager


class Priority(models.Model):
    """Priority model."""

    name = models.CharField(
        choices=PriorityLevel.choices, max_length=50, default=PriorityLevel.LOW
    )
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = PriorityManager()

    class Meta:
        verbose_name = "priority"
        verbose_name_plural = "priorities"
        default_manager_name = "objects"

    @property
    def priority_level_colour(self) -> Optional[str]:
        """Set priority level color."""

        return {
            "LOW": "warning",
            "MEDIUM": "info",
            "HIGH": "success",
            "CRITICAL": "danger",
        }.get(self.name)

    def clean(self) -> Any:
        """Ensure name is unique."""

        if Priority.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError({"name": "A priority with this name already exists."})

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save method."""

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return the name."""

        return self.name


class Status(models.Model):
    """Status model."""

    name = models.CharField(
        choices=StatusType.choices, max_length=50, default=StatusType.PENDING
    )
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = StatusManager()

    class Meta:
        verbose_name = "status"
        verbose_name_plural = "statuses"
        default_manager_name = "objects"

    @property
    def status_colour(self) -> Optional[str]:
        """Set status color."""

        return {
            "PENDING": "warning",
            "IN_PROGRESS": "info",
            "COMPLETED": "success",
            "CANCELLED": "danger",
        }.get(self.name)

    def __str__(self) -> str:
        """Return the name."""

        return self.name

    def clean(self) -> None:
        """Ensure name is unique."""

        if Status.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError({"name": "A status with this name already exists."})

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save method."""

        self.full_clean()
        super().save(*args, **kwargs)


class Task(models.Model):
    """Status model."""

    title = models.CharField(max_length=250)
    due_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    priority = models.ForeignKey(
        Priority, related_name="priority_task", on_delete=models.CASCADE
    )
    status = models.ForeignKey(
        Status, related_name="task_status", on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        CustomUser, related_name="task_assigned", on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        CustomUser, related_name="task_created", on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        CustomUser, related_name="task_status", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = TaskManager()

    class Meta:
        verbose_name = "task"
        verbose_name_plural = "tasks"
        default_manager_name = "objects"

    def __str__(self) -> str:
        """Return the name."""

        return self.title

    def clean(self) -> None:
        """Ensure name is unique."""

        if self.due_date and self.due_date < self.created_at.date():
            raise ValidationError(
                {"due_date": "Due date cannot be earlier than the creation date."}
            )

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save method."""

        self.full_clean()
        super().save(*args, **kwargs)
