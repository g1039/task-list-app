"""Service layer for the core application."""

from typing import Any

from webapp.accounts.models import CustomUser, Reference


def create_user(
    *,
    first_name: str,
    middle_name: str,
    last_name: str,
    email: str,
    password: str,
) -> Any:
    """Create new user."""

    username = Reference.generate_username()

    user = CustomUser(
        username=username,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        email=email,
    )
    user.set_password(password)
    user.save()

    return user


def update_profile_details(
    *,
    user: Any,
    first_name: str,
    middle_name: str,
    last_name: str,
    email: str,
) -> None:
    """Update the provided user's profile details."""

    user.first_name = first_name
    user.middle_name = middle_name
    user.last_name = last_name
    user.email = email
    user.save()
