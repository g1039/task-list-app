"""Custom managers/query layer for the tasktrack application."""

from typing import Any

from django.contrib.auth.models import BaseUserManager
from django.db import models

from webapp.tasktrack.enums import PriorityLevel, StatusType


class PriorityQuerySet(models.QuerySet):
    """Custom queryset for the priority model."""

    pass


class PriorityManager(BaseUserManager):
    """Custom manager for the priority model."""

    def get_queryset(self) -> Any:
        """Return custom query set based on self.model."""

        return PriorityQuerySet(self.model, using=self._db)


class StatusQuerySet(models.QuerySet):
    """Custom queryset for the status model."""

    pass


class StatusManager(BaseUserManager):
    """Custom manager for the priority model."""

    def get_queryset(self) -> Any:
        """Return custom query set based on self.model."""

        return StatusQuerySet(self.model, using=self._db)


class TaskQuerySet(models.QuerySet):
    """Custom queryset for the task model."""

    def low_priority_tasks(self) -> Any:
        """Return only the low priority tasks."""

        return self.filter(priority__name=PriorityLevel.LOW)

    def medium_priority_tasks(self) -> Any:
        """Return only the medium priority tasks."""

        return self.filter(priority__name=PriorityLevel.MEDIUM)

    def high_priority_tasks(self) -> Any:
        """Return only the high priority tasks."""

        return self.filter(priority__name=PriorityLevel.HIGH)

    def critical_priority_tasks(self) -> Any:
        """Return only the critical priority tasks."""

        return self.filter(priority__name=PriorityLevel.CRITICAL)

    def pending_tasks(self) -> Any:
        """Return only the pending tasks."""

        return self.filter(status__name=StatusType.PENDING)

    def in_progress_tasks(self) -> Any:
        """Return only the in progress tasks."""

        return self.filter(status__name=StatusType.IN_PROGRESS)

    def completed_tasks(self) -> Any:
        """Return only the completed tasks."""

        return self.filter(status__name=StatusType.COMPLETED)

    def cancelled_tasks(self) -> Any:
        """Return only the cancelled tasks."""

        return self.filter(status__name=StatusType.CANCELLED)


class TaskManager(BaseUserManager):
    """Custom manager for the task model."""

    def get_queryset(self) -> Any:
        """Return custom query set based on self.model."""

        return TaskQuerySet(self.model, using=self._db)
