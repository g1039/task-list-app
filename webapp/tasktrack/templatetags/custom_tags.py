"""Custom template filter."""

from typing import Any

from django import template

register = template.Library()


@register.filter
def user_display(user: Any, logged_in_user: Any) -> Any:
    """Return 'Me' if the user is the logged-in user, otherwise returns the full name."""

    if user == logged_in_user:
        return "Me"
    return user.get_full_names()
