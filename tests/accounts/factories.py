"""Factories for the accounts application."""

from typing import Any

from factory import PostGenerationMethodCall, Sequence, faker
from factory.django import DjangoModelFactory

from webapp.accounts.models import CustomUser


class CustomUserFactory(DjangoModelFactory):
    """Generate custom user instances for testing."""

    username = Sequence(lambda n: f"user-{n}")
    first_name = faker.Faker("first_name")
    middle_name = faker.Faker("first_name")
    last_name = faker.Faker("last_name")
    email = faker.Faker("email")
    password = PostGenerationMethodCall("set_password", "password")
    is_superuser = False
    is_staff = False
    is_active = True

    class Meta:
        model = CustomUser
        django_get_or_create = ("username",)

    @classmethod
    def admin_user(cls, commit: bool = False, **extra: Any) -> Any:
        """Create an admin user.

        If commit is True the record will be persisted to the database.
        """

        kwargs = {
            **extra,
            "is_superuser": True,
            "is_staff": True,
            "is_active": True,
        }

        if commit is True:
            return cls(**kwargs)
        else:
            return cls.build(**kwargs)
