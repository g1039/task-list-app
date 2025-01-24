"""Contains the application template based views."""

from typing import Any

from django.contrib.auth import logout as auth_logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import FormView

from webapp.accounts import services
from webapp.accounts.forms import (
    ProfileDetailsForm,
    RegistrationForm,
    UserPasswordChangeForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
)
from webapp.accounts.mixins import ReadOnlyThemedFormMixin
from webapp.accounts.parsers import parse_boolean


class LoginView(auth_views.LoginView):
    """User login view."""

    template_name = "accounts/auth-signin.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")


class RegisterView(FormView):
    """User registration view."""

    template_name = "accounts/auth-signup.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form: RegistrationForm) -> HttpResponseRedirect:
        """Update the user profile details."""

        first_name = form.cleaned_data["first_name"]
        middle_name = form.cleaned_data["middle_name"]
        last_name = form.cleaned_data["last_name"]
        email = form.cleaned_data["email"]
        password_2 = form.cleaned_data["password_2"]

        services.create_user(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            password=password_2,
        )
        return super().form_valid(form=form)


class UserPasswordResetView(auth_views.PasswordResetView):
    """User password reset view."""

    template_name = "accounts/forgot-password.html"
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """User password reset confirm view."""

    template_name = "accounts/recover-password.html"
    form_class = UserSetPasswordForm


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """User reset complete view."""

    template_name = "accounts/password_reset_complete.html"


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """User password reset done view."""

    template_name = "accounts/password_reset_done.html"


class UserPasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    """User password change view."""

    template_name = "accounts/password_change.html"
    form_class = UserPasswordChangeForm


class UserPasswordChangeDoneView(LoginRequiredMixin, auth_views.PasswordChangeDoneView):
    """User password change done view."""

    template_name = "accounts/password_change_done.html"


@login_required
@require_http_methods(["POST", "GET"])
def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """Log the requesting user out."""

    auth_logout(request)
    return HttpResponseRedirect(reverse("home"))


class ProfileDetailView(LoginRequiredMixin, ReadOnlyThemedFormMixin, FormView):
    """Profile detail section."""

    template_name = "profile/user-profile.html"
    form_class = ProfileDetailsForm
    success_url = reverse_lazy("profile-detail")

    def get_is_editable(self) -> bool:
        """If True the form fields will be disabled."""

        return parse_boolean(self.request.GET.get("editable", False))

    def get_initial(self) -> Any:
        """Return the initial data to use for forms on this view."""

        return {
            "first_name": self.request.user.first_name,
            "middle_name": self.request.user.middle_name,
            "last_name": self.request.user.last_name,
            "email": self.request.user.email,
        }

    def form_valid(self, form: ProfileDetailsForm) -> HttpResponseRedirect:
        """Update the user profile details."""

        first_name = form.cleaned_data["first_name"]
        middle_name = form.cleaned_data["middle_name"]
        last_name = form.cleaned_data["last_name"]
        email = form.cleaned_data["email"]

        services.update_profile_details(
            user=self.request.user,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
        )
        return super().form_valid(form=form)


register_view = RegisterView.as_view()
login_view = LoginView.as_view()
user_password_reset_view = UserPasswordResetView.as_view()
user_password_reset_confirm_view = UserPasswordResetConfirmView.as_view()
password_reset_complete_view = PasswordResetCompleteView.as_view()
password_reset_done_view = PasswordResetDoneView.as_view()
user_password_change_view = UserPasswordChangeView.as_view()
user_password_change_done_view = UserPasswordChangeDoneView.as_view()
profile_detail_view = ProfileDetailView.as_view()
