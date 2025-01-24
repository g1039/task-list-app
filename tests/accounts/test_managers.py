import pytest
from django.contrib.auth.models import Permission
from django.test import override_settings

from tests.accounts.factories import CustomUserFactory
from webapp.accounts.models import CustomUser


class TestCustomUserManager:
    @pytest.mark.django_db
    def test_get_user_from_url_safe_id(self) -> None:
        user = CustomUserFactory()
        result = CustomUser.objects.get_user_from_url_safe_id(
            b64_user_id=user.url_safe_b64_encoded_id
        )
        assert user == result

    @pytest.mark.django_db
    def test_get_user_from_url_safe_id_not_found(self) -> None:
        result = CustomUser.objects.get_user_from_url_safe_id(b64_user_id="testing")
        assert result is None

    @pytest.mark.django_db
    def test_create_user(self) -> None:
        user = CustomUser.objects.create_user(
            username="testing",
            password="testing",
        )
        assert isinstance(user, CustomUser)
        assert user.is_staff is False
        assert user.is_superuser is False

    @pytest.mark.django_db
    def test_create_superuser(self) -> None:
        user = CustomUser.objects.create_superuser(
            username="testing",
            password="testing",
        )
        assert isinstance(user, CustomUser)
        assert user.is_staff is True
        assert user.is_superuser is True

    @pytest.mark.django_db
    def test_with_perm_active(self) -> None:
        """Ensure that active user path returns the expected user."""

        permission = Permission.objects.filter(codename="view_customuser").first()
        CustomUserFactory(username="user-1", password="testing", is_active=True)
        user = CustomUserFactory(username="user-2", password="testing", is_active=True)
        user.user_permissions.add(permission)
        queryset = CustomUser.objects.with_perm(
            perm=permission,
            is_active=True,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        assert queryset.count() == 1
        assert queryset.first() == user

    @pytest.mark.django_db
    def test_with_perm_is_active_false(self) -> None:
        """Ensure that inactive user path returns no users."""

        permission = Permission.objects.filter(codename="view_customuser").first()
        user_1 = CustomUserFactory(
            username="user-1", password="testing", is_active=False
        )
        user_2 = CustomUserFactory(
            username="user-2", password="testing", is_active=False
        )
        user_1.user_permissions.add(permission)
        user_2.user_permissions.add(permission)
        queryset = CustomUser.objects.with_perm(
            perm=permission,
            is_active=True,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        assert queryset.count() == 0

    def test_create_superuser_is_staff_raises(self) -> None:
        with pytest.raises(ValueError):
            CustomUser.objects.create_superuser(
                username="testing", password="testing", is_staff=False
            )

    def test_create_superuser_is_superuser_raises(self) -> None:
        with pytest.raises(ValueError):
            CustomUser.objects.create_superuser(
                username="testing", password="testing", is_superuser=False
            )

    @override_settings(
        AUTHENTICATION_BACKENDS=["django.contrib.auth.backends.ModelBackend"]
    )
    @pytest.mark.django_db
    def test_with_perm_single_backend(self) -> None:
        permission = Permission.objects.filter(codename="view_customuser").first()
        user_1 = CustomUserFactory(
            username="user-1", password="testing", is_active=True
        )
        user_2 = CustomUserFactory(
            username="user-2", password="testing", is_active=False
        )
        user_1.user_permissions.add(permission)
        user_2.user_permissions.add(permission)
        queryset = CustomUser.objects.with_perm(
            perm=permission,
            is_active=True,
        )
        assert queryset.count() == 1

    @pytest.mark.django_db
    def test_with_perm_backend_type_raises(self) -> None:
        permission = Permission.objects.filter(codename="view_customuser").first()
        with pytest.raises(TypeError):
            CustomUser.objects.with_perm(perm=permission, is_active=True, backend=True)  # type: ignore
