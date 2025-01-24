"""Contains the application template based views."""

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    """Home page view."""

    template_name = "pages/index.html"

    def get_context_data(self, **kwargs: Any) -> Any:
        """Add context for the view."""

        context = super().get_context_data(**kwargs)

        return context


home_view = HomeView.as_view()
