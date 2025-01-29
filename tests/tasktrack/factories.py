"""Factories for the tasktrack application."""

from zoneinfo import ZoneInfo

from django.conf import settings
from factory import SubFactory, faker, fuzzy
from factory.django import DjangoModelFactory

from tests.accounts.factories import CustomUserFactory
from webapp.tasktrack.enums import PriorityLevel, StatusType
from webapp.tasktrack.models import Priority, Status, Task

TZINFO = ZoneInfo(settings.TIME_ZONE)


class PriorityFactory(DjangoModelFactory):

    name = fuzzy.FuzzyChoice(PriorityLevel.choices, getter=lambda x: x[0])
    description = fuzzy.FuzzyText()

    class Meta:
        model = Priority


class StatusFactory(DjangoModelFactory):

    name = fuzzy.FuzzyChoice(StatusType.choices, getter=lambda x: x[0])
    description = fuzzy.FuzzyText()

    class Meta:
        model = Status


class TaskFactory(DjangoModelFactory):

    title = fuzzy.FuzzyText()
    due_date = faker.Faker("date")
    description = fuzzy.FuzzyText()
    priority = SubFactory(PriorityFactory)
    status = SubFactory(StatusFactory)
    assigned_to = SubFactory(CustomUserFactory)
    created_by = SubFactory(CustomUserFactory)
    updated_by = SubFactory(CustomUserFactory)
    created_at = faker.Faker("date_time", tzinfo=TZINFO)
    updated_at = faker.Faker("date_time", tzinfo=TZINFO)

    class Meta:
        model = Task
