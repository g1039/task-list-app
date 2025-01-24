"""Custom managers/query layer for the accounts application."""

from typing import Any, Optional

from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils.encoding import DjangoUnicodeDecodeError, force_str
from django.utils.http import urlsafe_base64_decode


class CustomUserQuerySet(models.QuerySet):
    """Custom queryset for the custom user model."""

    pass


class CustomUserManager(BaseUserManager):
    """Custom manager for the custom user model."""

    use_in_migrations = True

    def get_queryset(self) -> Any:
        """Return custom query set based on self.model."""

        return CustomUserQuerySet(self.model, using=self._db)

    def get_user_from_url_safe_id(self, *, b64_user_id: str) -> Optional[Any]:
        """Retrieve a user given the provided b64 encoded url safe user id."""

        try:
            user_id = force_str(urlsafe_base64_decode(b64_user_id))
        except (AttributeError, DjangoUnicodeDecodeError):
            return None
        return self.get_queryset().filter(pk=user_id).first()

    def create_user(
        self, username: str, password: Optional[str] = None, **extra_fields: Any
    ) -> Any:
        """Generate a user instance."""

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username: str, password: Optional[str] = None, **extra_fields: Any
    ) -> Any:
        """Generate a super user instance."""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username=username, password=password, **extra_fields)

    def with_perm(
        self,
        perm: Any,
        is_active: bool = True,
        include_superusers: bool = True,
        backend: Optional[str] = None,
        obj: Any = None,
    ) -> Any:
        """Return the set of users with the specified permission."""

        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                auth_backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                f"backend must be a dotted import path string (got {backend!r})."
            )
        else:
            auth_backend = auth.load_backend(backend)
        if hasattr(auth_backend, "with_perm"):
            return auth_backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()
