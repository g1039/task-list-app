"""Enums for hardcoded choice field data."""

from typing import Any

from django.db import models


class PriorityLevel(models.TextChoices):
    """Enumeration class for priority level."""

    LOW: Any = "LOW", "Low"
    MEDIUM: Any = "MEDIUM", "Medium"
    HIGH: Any = "HIGH", "High"
    CRITICAL: Any = "CRITICAL", "Critical"


class StatusType(models.TextChoices):
    """Enumeration class for status type."""

    PENDING: Any = "PENDING", "Pending"
    IN_PROGRESS: Any = "IN_PROGRESS", "In Progress"
    COMPLETED: Any = "COMPLETED", "Completed"
    CANCELLED: Any = "CANCELLED", "Cancelled"
