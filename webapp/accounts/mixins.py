"""Custom mixin classes for application wide usage."""

from typing import Any, Dict

from django.forms.utils import ErrorList
from django.utils.html import format_html
from django.views.generic.edit import FormMixin


class ThemedErrorList(ErrorList):
    """Add the project theme to the error list."""

    def _init_(self, *args: Any, **kwargs: Any) -> None:
        """Add the appropriate CSS class."""

        kwargs["error_class"] = "invalid-feedback"
        super()._init_(*args, **kwargs)

    def as_span(self) -> str:
        """Render the error as a span."""

        error = "\n".join(f'<p class="m-0">{error}</p>' for error in self)

        if not error:
            return ""

        return format_html(f'<span class="{self.error_class}">{error}</span>')


class ThemedFormMixin(FormMixin):
    """Apply the project theme where applicable in form views."""

    def get_form_kwargs(self) -> Dict[str, Any]:
        """Apply the project theme where applicable in form views."""

        kwargs = super().get_form_kwargs()
        kwargs["error_class"] = ThemedErrorList
        return kwargs


class ReadOnlyThemedFormMixin(ThemedFormMixin):
    """Make any form read only from a view."""

    is_editable = False

    def get_is_editable(self) -> bool:
        """If True the form fields will be disabled."""

        return self.is_editable

    def get_form(self, form_class: Any = None) -> Any:
        """Set all form fields to read only."""

        form = super().get_form()

        if self.get_is_editable() is True:
            return form

        for field in form.fields:
            form.fields[field].widget.attrs["disabled"] = "disabled"

        return form

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add the form_enabled attribute to the context."""

        context = super().get_context_data(**kwargs)
        context["is_editable"] = self.get_is_editable()
        return context
