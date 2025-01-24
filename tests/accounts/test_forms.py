from unittest.mock import patch

import pytest
from django.contrib.auth.forms import AuthenticationForm

from tests.accounts.factories import CustomUserFactory
from webapp.accounts.forms import CustomUserCreationForm


@pytest.mark.django_db
def test_custom_user_creation_form() -> None:
    with patch(
        "webapp.accounts.forms.Reference.generate_username"
    ) as mock_generate_username:
        mock_generate_username.return_value = "user-1"
        form = CustomUserCreationForm(
            {
                "email": "testing@mail.com",
                "password1": "@Mypassword123",
                "password2": "@Mypassword123",
            }
        )
        form.is_valid()
        user = form.save()
        assert user.username == "user-1"


@pytest.mark.django_db
def test_email_is_unique() -> None:
    user = CustomUserFactory(email="foo@mail.com")
    form = CustomUserCreationForm(
        data={
            "email": user.email,
            "password": "@Mypassword123",
        }
    )
    errors = form.errors["email"]
    assert errors[0] == "A user with that email address already exists."


class TestLoginForm:
    @pytest.mark.django_db
    def test_valid(self) -> None:
        CustomUserFactory(email="foo@mail.com", password="@Mypassword123")
        form = AuthenticationForm(
            data={
                "username": "foo@mail.com",
                "password": "@Mypassword123",
            }
        )
        assert form.is_valid() is True

    @pytest.mark.django_db
    def test_invalid_wrong_email(self) -> None:
        CustomUserFactory(email="foo@mail.com", password="@Mypassword123")
        form = AuthenticationForm(
            data={
                "username": "bob@mail.com",
                "password": "@Mypassword123",
            }
        )

        assert form.is_valid() is False
        assert len(form.errors) == 1

    @pytest.mark.django_db
    def test_invalid_user_not_found(self) -> None:
        CustomUserFactory(password="@Mypassword123")
        form = AuthenticationForm(
            data={
                "username": "bobmartin@mail.com",
                "password": "@Mypassword123",
            }
        )

        assert form.is_valid() is False
        assert len(form.errors) == 1
        assert form.errors == {
            "__all__": [
                "Please enter a correct username and password. Note that both fields may be case-sensitive."
            ]
        }

    @pytest.mark.django_db
    def test_invalid_no_email(self) -> None:
        CustomUserFactory(password="@Mypassword123")
        form = AuthenticationForm(
            data={
                "username": "",
                "password": "",
            }
        )

        assert form.is_valid() is False
        assert len(form.errors) == 2
        assert form.errors["username"] == ["This field is required."]
        assert form.errors["password"] == ["This field is required."]
