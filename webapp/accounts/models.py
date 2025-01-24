"""Database models for the accounts application."""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from webapp.accounts.managers import CustomUserManager


class Reference(models.Model):
    """Generate references for other models."""

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "reference"
        verbose_name_plural = "references"

    @classmethod
    def generate_reference(cls, prefix: str) -> str:
        """Generate a unique reference number."""

        instance = cls.objects.create()
        suffix = f"{instance.pk}".zfill(6)
        return f"{prefix}-{suffix}"

    @classmethod
    def generate_username(cls) -> str:
        """Generate a unique reference number."""

        return cls.generate_reference(prefix="user")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Models system user."""

    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(
        unique=True,
        error_messages={"unique": "A user with that email address already exists."},
        max_length=150,
        null=True,
        blank=True,
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Designates whether this user should be treated as active."
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []  # type: ignore

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        default_manager_name = "objects"

    def __str__(self) -> str:
        """Return the username."""

        return self.username

    def clean(self) -> None:
        """Normalise the provided email."""

        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def url_safe_b64_encoded_id(self) -> str:
        """Encode the user id as a b64 url safe string."""

        return urlsafe_base64_encode(force_bytes(self.pk))

    def first_names(self) -> str:
        """Return the user first and middle names as a single str."""

        names = [self.first_name, self.middle_name]
        return " ".join(name for name in names if name)

    def get_full_names(self) -> str:
        """Return the full name for standard user model compatibility."""

        names = [self.first_name, self.middle_name, self.last_name]
        return " ".join(name for name in names if name)

    def get_short_name(self) -> str:
        """Return the short name for standard user model compatibility."""

        return self.first_name
