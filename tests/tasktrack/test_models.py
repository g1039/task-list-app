import pytest

from tests.tasktrack.factories import PriorityFactory, StatusFactory, TaskFactory
from webapp.tasktrack.enums import PriorityLevel, StatusType


@pytest.mark.django_db
def test_priority_str_() -> None:
    instance = PriorityFactory.build()
    assert str(instance) == instance.name

    low_priority = PriorityFactory(name=PriorityLevel.LOW)
    medium_priority = PriorityFactory(name=PriorityLevel.MEDIUM)
    high_priority = PriorityFactory(name=PriorityLevel.HIGH)
    critical_priority = PriorityFactory(name=PriorityLevel.CRITICAL)

    low_priority.save()
    medium_priority.save()
    high_priority.save()
    critical_priority.save()

    assert str(low_priority) == PriorityLevel.LOW
    assert str(medium_priority) == PriorityLevel.MEDIUM
    assert str(high_priority) == PriorityLevel.HIGH
    assert str(critical_priority) == PriorityLevel.CRITICAL


@pytest.mark.django_db
def test_status_str_() -> None:
    instance = StatusFactory.build()
    assert str(instance) == instance.name

    pending = StatusFactory(name=StatusType.PENDING)
    in_progress = StatusFactory(name=StatusType.IN_PROGRESS)
    completed = StatusFactory(name=StatusType.COMPLETED)
    cancelled = StatusFactory(name=StatusType.CANCELLED)

    pending.save()
    in_progress.save()
    completed.save()
    cancelled.save()

    assert str(pending) == StatusType.PENDING
    assert str(in_progress) == StatusType.IN_PROGRESS
    assert str(completed) == StatusType.COMPLETED
    assert str(cancelled) == StatusType.CANCELLED


def test_task_str_() -> None:
    instance = TaskFactory.build()
    assert str(instance) == instance.title
