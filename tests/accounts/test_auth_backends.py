from typing import Any, Optional

import pytest
from django.test import RequestFactory

from tests.accounts.factories import CustomUserFactory
from webapp.accounts.auth.backends import EmailBackend


@pytest.fixture
def mock_request(rf: RequestFactory) -> Any:
    """Mock out the user model."""

    return rf.post("some-url")


class TestEmailBackend:
    @pytest.mark.parametrize("username", ["", None])
    def test_username_bad(self, username: Optional[str], mock_request: Any) -> None:
        backend = EmailBackend()
        result = backend.authenticate(mock_request, username=username, password="foo")
        assert result is None

    @pytest.mark.parametrize("password", ["", None])
    def test_password_bad(self, password: Optional[str], mock_request: Any) -> None:
        backend = EmailBackend()
        result = backend.authenticate(
            mock_request, username="foo@mail.com", password=password
        )
        assert result is None

    @pytest.mark.django_db
    def test_user_does_not_exist(self, mock_request: Any) -> None:
        backend = EmailBackend()
        result = backend.authenticate(
            mock_request, username="foo@mail.com", password="foo"
        )
        assert result is None

    @pytest.mark.django_db
    def test_user_exist(self, mock_request: Any) -> None:
        password = "foo"
        email = "foo@mail.com"
        user = CustomUserFactory(email=email, password=password)
        backend = EmailBackend()
        expected_user = backend.authenticate(
            mock_request, username=email, password=password
        )
        assert user == expected_user

    @pytest.mark.django_db
    def test_user_not_active(self, mock_request: Any) -> None:
        password = "foo"
        email = "foo"
        CustomUserFactory(email=email, password=password, is_active=False)
        backend = EmailBackend()
        result = backend.authenticate(mock_request, username=email, password=password)
        assert result is None
