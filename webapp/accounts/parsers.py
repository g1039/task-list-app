"""Parser classes for model field parsing."""

from typing import Any

from django.forms.fields import BooleanField


def parse_boolean(value: Any) -> bool:
    """Convert the provided value to a boolean."""

    field = BooleanField()
    return field.to_python(value)
