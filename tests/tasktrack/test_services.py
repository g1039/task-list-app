import datetime

import pytest
from django.utils import timezone

from tests.accounts.factories import CustomUserFactory
from tests.tasktrack.factories import PriorityFactory, StatusFactory, TaskFactory
from webapp.tasktrack import services
from webapp.tasktrack.enums import StatusType
from webapp.tasktrack.models import Task


@pytest.mark.django_db
def test_create_pressure_header() -> None:

    user = CustomUserFactory()
    priority = PriorityFactory()
    status = StatusFactory(name=StatusType.PENDING)
    task = TaskFactory(due_date=timezone.now().date(), status=status, priority=priority)
    services.create_task(
        user=user,
        title=task.title,
        due_date=task.due_date,
        description=task.description,
        priority=task.priority,
        assigned_to=task.assigned_to,
    )

    assert Task.objects.filter(priority=priority).exists()
    filter_task = Task.objects.filter(priority=priority).first()
    assert filter_task.priority == priority


@pytest.mark.django_db
def test_update_task_successful() -> None:

    user = CustomUserFactory()
    task = TaskFactory(
        due_date=datetime.date(2025, 12, 1),
        assigned_to=user,
        created_at=timezone.now().date(),
    )

    services.update_task(user=user, pk=task.pk)

    updated_task = Task.objects.get(pk=task.pk)

    assert updated_task.updated_by == user
    assert updated_task.updated_at.date() == timezone.now().date()
    assert updated_task.updated_at > task.updated_at
