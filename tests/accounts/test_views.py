from http import HTTPStatus
from unittest.mock import Mock

import pytest
from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory
from django.urls import reverse

from tests.accounts.factories import CustomUserFactory
from webapp.accounts.views import ProfileDetailView

User = get_user_model()


class TestLoginView:
    @pytest.mark.django_db
    def test_get(self, client: Client) -> None:
        response = client.get(reverse("login"))

        assert response.status_code == HTTPStatus.OK

    @pytest.mark.django_db
    def test_post(self, client: Client) -> None:
        user = CustomUserFactory(is_active=True)
        url = reverse(
            "login",
        )
        response = client.post(
            url,
            {
                "username": user.email,
                "password": user.password,
            },
        )
        assert response.status_code == HTTPStatus.OK


class TestLogoutView:
    @pytest.mark.django_db
    def test_logout_view_post(self, client: Client) -> None:
        """Integration test to ensure a user can logout."""
        user = CustomUserFactory(is_active=True)
        client.force_login(user)
        response = client.post(reverse("logout"))
        assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_register_view(client: Client) -> None:

    payload = {
        "email": "foo@mail.com",
        "password1": "@Mypassword123",
        "password2": "@Mypassword123",
    }
    url = reverse("register")
    response = client.post(url, data=payload)

    assert response.status_code == HTTPStatus.OK


class TestProfileDetailView:
    def test_get_initial(self, rf: RequestFactory) -> None:

        user = CustomUserFactory.build()
        request = rf.get("some-url")
        request.user = user
        view = ProfileDetailView(request=request)
        expected_result = {
            "first_name": user.first_name,
            "middle_name": user.middle_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        actual_result = view.get_initial()
        assert actual_result == expected_result

    @pytest.mark.django_db
    def test_get_is_editable(self, rf: RequestFactory) -> None:
        request = rf.get("some-url")
        request.user = CustomUserFactory(is_active=True)
        view = ProfileDetailView(request=request)
        response = view.get_is_editable()
        assert type(response) == bool

    @pytest.mark.django_db
    def test_form_valid(self, rf: RequestFactory) -> None:
        user = CustomUserFactory(is_active=True, last_name="Zuckerberg")
        request = rf.get("some-url")
        form = Mock()
        form.cleaned_data = {
            "first_name": user.first_name,
            "middle_name": user.middle_name,
            "last_name": "Jones",
            "email": user.email,
        }
        request.user = user

        view = ProfileDetailView(request=request)

        response = view.form_valid(form)

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("profile-detail")
