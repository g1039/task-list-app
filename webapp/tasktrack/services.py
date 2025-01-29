"""Service layer for the tasktrack application."""

from typing import Any

from django.utils import timezone

from webapp.tasktrack.enums import StatusType
from webapp.tasktrack.models import Status, Task


def create_task(
    *,
    user: Any,
    title: str,
    due_date: Any,
    description: str,
    priority: Any,
    assigned_to: Any
) -> None:
    """Create new task."""

    status = Status.objects.filter(name=StatusType.PENDING).first()

    task = Task(
        title=title,
        due_date=due_date,
        description=description,
        priority=priority,
        status=status,
        assigned_to=assigned_to,
        created_by=user,
        updated_by=user,
    )
    task.save()


def update_task(*, user: Any, pk: int) -> None:
    """Update task."""

    task = Task.objects.get(pk=pk)

    task.updated_by = user
    task.updated_at = timezone.now()
    task.save()
