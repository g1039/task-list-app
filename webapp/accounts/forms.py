"""Form classes for the accounts application."""

from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.password_validation import validate_password

from webapp.accounts.models import CustomUser, Reference

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form for use in the admin panel."""

    class Meta:
        model = User
        fields = ("email",)
        field_classes = {"email": forms.EmailField}

    def save(self, commit: bool = True) -> Any:
        """Generate a new user.

        This form is meant to be used with the django admin panel.
        """

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = Reference.generate_username()

        if commit:
            user.save()
        return user


class RegistrationForm(forms.Form):
    """User registration form."""

    first_name = forms.CharField(
        required=True,
    )
    middle_name = forms.CharField(
        required=False,
    )
    last_name = forms.CharField(
        required=True,
    )
    email = forms.EmailField(
        required=True,
    )
    password_1 = forms.CharField(
        label="Password", strip=False, widget=forms.PasswordInput
    )
    password_2 = forms.CharField(
        label="Password Confirmation",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Enter the same password as before, for verification.",
    )

    def clean_email(self) -> str:
        """Validate the provided email."""

        email = self.cleaned_data.get("email")

        if CustomUser.objects.filter(email=email.lower()).exists():
            self.add_error("email", "A user with that email address already exists.")

        return email

    def clean_password_2(self) -> str:
        """Validate the provided password."""

        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")

        if password_1 and password_2 and password_1 != password_2:
            self.add_error("password_2", "The two password fields didn't match")

        return password_2

    def clean_password_1(self) -> str:
        """Validate the provided password."""

        password_1 = self.cleaned_data.get("password_1", None)
        validate_password(password=password_1)

        return password_1


class UserPasswordResetForm(PasswordResetForm):
    """User password reset form."""

    email = forms.EmailField(
        required=True,
    )


class UserSetPasswordForm(SetPasswordForm):
    """User set password form."""

    new_password1 = forms.CharField(
        label="New Password", strip=False, widget=forms.PasswordInput
    )

    new_password2 = forms.CharField(
        label="Confirm New Password", strip=False, widget=forms.PasswordInput
    )

    def clean_new_password2(self) -> str:
        """Validate the provided password."""

        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error("new_password2", "The two password fields didn't match")

        return new_password2


class UserPasswordChangeForm(PasswordChangeForm):
    """User password change form."""

    old_password = forms.CharField(
        label="Old Password", strip=False, widget=forms.PasswordInput
    )

    new_password1 = forms.CharField(
        label="New Password", strip=False, widget=forms.PasswordInput
    )

    new_password2 = forms.CharField(
        label="Confirm New Password", strip=False, widget=forms.PasswordInput
    )

    def clean_new_password2(self) -> str:
        """Validate the provided password."""

        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error("new_password2", "The two password fields didn't match")

        return new_password2

    def clean_new_password1(self) -> str:
        """Validate the provided password."""

        new_password1 = self.cleaned_data.get("new_password1", None)
        validate_password(password=new_password1)

        return new_password1


class ProfileDetailsForm(forms.Form):
    """Read only form with user profile details."""

    first_name = forms.CharField(
        disabled=False,
        required=True,
    )
    middle_name = forms.CharField(
        disabled=False,
        required=False,
    )
    last_name = forms.CharField(
        disabled=False,
        required=True,
    )
    email = forms.EmailField(
        disabled=False,
        required=True,
    )
