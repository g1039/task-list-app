import pytest

from tests.accounts.factories import CustomUserFactory
from webapp.tasktrack.templatetags.custom_tags import user_display


@pytest.mark.django_db
def test_user_display_returns_me_for_logged_in_user() -> None:

    logged_in_user = CustomUserFactory()

    result = user_display(logged_in_user, logged_in_user)

    assert result == "Me"


@pytest.mark.django_db
def test_user_display_returns_full_name_for_other_users() -> None:

    logged_in_user = CustomUserFactory()
    other_user = CustomUserFactory(first_name="John", last_name="Doe")

    result = user_display(other_user, logged_in_user)

    assert result == other_user.get_full_names()


@pytest.mark.django_db
def test_user_display_handles_anonymous_user() -> None:
    class AnonymousUser:
        def get_full_names(self) -> str:
            return "Anonymous"

    anonymous_user = AnonymousUser()
    logged_in_user = CustomUserFactory()

    result = user_display(anonymous_user, logged_in_user)

    assert result == "Anonymous"
