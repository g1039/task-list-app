"""Provides a decorator to restrict access to a view to superusers only."""

from functools import wraps
from typing import Any

from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse


def limit_access(view_func: Any) -> Any:
    """Restrict access to a view to superusers only."""

    @wraps(view_func)
    def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        if not request.user.is_superuser:
            # messages.error(request, "Access denied. You need superuser privileges to view this page.")
            return redirect(reverse("home"))

        return view_func(request, *args, **kwargs)

    return wrapper
