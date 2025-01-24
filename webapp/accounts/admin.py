"""Admin panel for the accounts application."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from webapp.accounts.forms import CustomUserCreationForm

User = get_user_model()

FIELDSETS = (
    (None, {"fields": ("password",)}),
    (
        _("Personal info"),
        {
            "fields": (
                "username",
                "first_name",
                "last_name",
                "middle_name",
            )
        },
    ),
    (
        _("Contact info"),
        {"fields": ("email",)},
    ),
    (
        _("Permissions"),
        {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        },
    ),
    (_("Important dates"), {"fields": ("last_login", "date_joined")}),
)

ADD_FIELDSETS = (
    (
        None,
        {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        },
    ),
)


@admin.register(User)
class CustomUser(admin.ModelAdmin):
    """Custom admin for the custom user model."""

    add_form = CustomUserCreationForm
    fieldsets = FIELDSETS
    add_fieldsets = ADD_FIELDSETS
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
    )
    readonly_fields = ("username",)
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("-pk",)
