from typing import Any

import pytest

from webapp.tasktrack.enums import PriorityLevel, StatusType


def test_priority_level_choices() -> None:
    expected_choices = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    ]
    actual_choices = PriorityLevel.choices
    assert actual_choices == expected_choices


@pytest.mark.parametrize(
    "choice, expected_label",
    [
        (PriorityLevel.LOW, "Low"),
        (PriorityLevel.MEDIUM, "Medium"),
        (PriorityLevel.HIGH, "High"),
        (PriorityLevel.CRITICAL, "Critical"),
    ],
)
def test_priority_level_labels(choice: Any, expected_label: str) -> None:
    assert choice.label == expected_label


def test_status_type_choices() -> None:
    expected_choices = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]
    actual_choices = StatusType.choices
    assert actual_choices == expected_choices


@pytest.mark.parametrize(
    "choice, expected_label",
    [
        (StatusType.PENDING, "Pending"),
        (StatusType.IN_PROGRESS, "In Progress"),
        (StatusType.COMPLETED, "Completed"),
        (StatusType.CANCELLED, "Cancelled"),
    ],
)
def test_status_type_labels(choice: Any, expected_label: str) -> None:
    assert choice.label == expected_label
