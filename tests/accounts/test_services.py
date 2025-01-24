import pytest

from tests.accounts.factories import CustomUserFactory
from webapp.accounts import services
from webapp.accounts.models import CustomUser


@pytest.mark.django_db
def test_create_custom_user() -> None:
    """Ensure the create user service creates a user."""

    services.create_user(
        first_name="Test",
        middle_name="Test",
        last_name="Test",
        email="testing@domain.com",
        password="testing",
    )
    assert CustomUser.objects.filter(email="testing@domain.com").exists()
    user = CustomUser.objects.filter(email="testing@domain.com").first()
    assert user.first_name == "Test"
    assert user.middle_name == "Test"
    assert user.last_name == "Test"


@pytest.mark.django_db
def test_update_profile_details() -> None:
    """Ensure the profile details are updated."""

    user = CustomUserFactory(
        first_name="Ntu2ko",
        last_name="Dhlamini",
    )
    services.update_profile_details(
        user=user,
        first_name="Ntuthuko",
        middle_name=user.middle_name,
        last_name="Dlamini",
        email=user.email,
    )

    user.refresh_from_db()
    assert user.first_name == "Ntuthuko"
    assert user.last_name == "Dlamini"
