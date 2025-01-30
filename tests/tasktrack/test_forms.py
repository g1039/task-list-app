import datetime
from typing import Any, Dict

import pytest
from django.utils import timezone

from tests.accounts.factories import CustomUserFactory
from tests.tasktrack.factories import PriorityFactory, StatusFactory
from webapp.tasktrack.forms import (
    CreateCalendarTaskForm,
    CreateTaskForm,
    TaskUpdateForm,
)


class TestCreateTaskForm:
    @pytest.mark.django_db
    def test_create_task(self) -> None:
        form = CreateTaskForm(
            data={
                "title": "Implement User Notifications Feature",
                "due_date": datetime.date(2025, 12, 1),
                "discription": "Develop a user notification system in the Django app to alert users about task updates and deadlines.",
                "priority": PriorityFactory(),
                "assigned_to": CustomUserFactory(),
                "ctreated_at": timezone.now().date(),
            },
        )

        assert form.is_valid() is True
        assert form.errors == {}

    @pytest.mark.django_db
    def test_priority_is_required(self) -> None:
        form = CreateTaskForm(
            data={
                "priority": "",
            },
        )
        errors = form.errors["priority"]
        assert errors[0] == "This field is required."

    @pytest.mark.django_db
    def test_assigned_to_is_required(self) -> None:
        form = CreateTaskForm(
            data={
                "assigned_to": "",
            },
        )
        errors = form.errors["assigned_to"]
        assert errors[0] == "This field is required."


class TestTaskUpdateForm:
    @pytest.mark.django_db
    def test_task_update(self) -> None:
        form = TaskUpdateForm(
            data={
                "title": "Add Calendar View for Task Management",
                "due_date": timezone.now().date(),
                "discription": "Create a calendar view in the Django app to display tasks based on their due dates.",
                "priority": PriorityFactory(),
                "status": StatusFactory(),
                "assigned_to": CustomUserFactory(),
            },
        )
        assert form.is_valid() is True
        assert form.errors == {}

    @pytest.mark.django_db
    def test_required_fields(self) -> None:
        form = TaskUpdateForm(
            data={"priority": "", "status": "", "assigned_to": ""},
        )
        priority_errors = form.errors["priority"]
        assert priority_errors[0] == "This field is required."
        status = form.errors["status"]
        assert status[0] == "This field is required."
        assigned_to = form.errors["assigned_to"]
        assert assigned_to[0] == "This field is required."


@pytest.mark.django_db
class TestCreateCalendarTaskForm:
    def test_valid_form_data(self) -> None:

        priority = PriorityFactory()
        assigned_to = CustomUserFactory()

        form_data = {
            "title": "New Task",
            "due_date": timezone.now().date(),
            "description": "Test description",
            "priority": priority,
            "assigned_to": assigned_to,
        }

        form = CreateCalendarTaskForm(data=form_data)
        assert form.is_valid(), form.errors

    def test_invalid_due_date_in_past(self) -> None:

        priority = PriorityFactory()
        assigned_to = CustomUserFactory()

        form_data = {
            "title": "New Task",
            "due_date": datetime.date.today() - datetime.timedelta(days=1),
            "description": "Test description",
            "priority": priority,
            "assigned_to": assigned_to,
        }

        form = CreateCalendarTaskForm(data=form_data)
        assert not form.is_valid()
        assert "due_date" in form.errors
        assert form.errors["due_date"] == [
            "Due date cannot be earlier than the creation date."
        ]

    def test_missing_required_fields(self) -> None:

        form_data: Dict[Any, Any] = {}

        form = CreateCalendarTaskForm(data=form_data)
        assert not form.is_valid()
        assert "title" in form.errors
        assert "priority" in form.errors
        assert "assigned_to" in form.errors
