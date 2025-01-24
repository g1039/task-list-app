"""Contains custom auth backends for the application."""

from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

User = get_user_model()


class EmailBackend(ModelBackend):
    """Custom auth backend which authenticates a user on their email address."""

    def authenticate(
        self,
        request: HttpRequest,
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs: Any,
    ) -> Optional[Any]:
        """Authenticate the user based on the provided email.

        Note the username input must be the user's email address. This naming
        convention allows the backend to integrate with the django login view
        and form.
        """

        if any([username is None, username == "", password is None, password == ""]):
            return None

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            User().set_password(password)
        else:
            conds = [
                user.check_password(password) is True,
                self.user_can_authenticate(user) is True,
            ]

            if all(conds):
                return user
            else:
                return None

        return None
