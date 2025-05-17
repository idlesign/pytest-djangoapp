from typing import Union

import pytest

from .utils import get_stamp

if False:  # pragma: nocover
    from django.contrib.auth.models import AbstractUser, AnonymousUser  # noqa


TypeUser = Union['AbstractUser', 'AnonymousUser']


@pytest.fixture()
def user_model() -> TypeUser:
    """Returns user model class.

    ```py
    def test_this(user_model):
        model_cls = user_model
    ```

    """
    from django.contrib.auth import get_user_model

    return get_user_model()


@pytest.fixture()
def user_create(user_model):
    """Allows Django user object generation.

    ```py
    def test_this(user_create):
        user = user_create()
    ```
    .. note:: User password is accessible via `password_plain` attribute.

    :param superuser: Whether to create a superuser.
    :param anonymous: Whether to create an anonymous user.
    :param attributes: Additional user object attributes to initialize.

    """
    from django.contrib.auth.models import AnonymousUser

    def user_create_(*, superuser: bool = False, anonymous: bool = False, attributes: dict = None) -> TypeUser:

        if anonymous:
            return AnonymousUser()

        attributes = attributes or {}
        manager = user_model._default_manager

        username = (('admin' if superuser else 'user') + '_' + get_stamp())

        kwargs = {
            'username': username,
            'email': f'{username}@example.com',
            'password': 'password',
        }

        kwargs.update(attributes)

        if superuser:
            user = manager.create_superuser(**kwargs)
        else:
            user = manager.create_user(**kwargs)

        # Keep plain password for test purposes.
        user.password_plain = kwargs['password']

        return user

    return user_create_


@pytest.fixture()
def user(user_create) -> TypeUser:
    """Exposes Django user object.

    Shortcut for `user_create` fixture.

    ```py
    def test_this(user):
        username = user.username
    ```

    .. note:: User password is accessible via `password_plain` attribute.

    """
    return user_create()
