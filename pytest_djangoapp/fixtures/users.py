# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from .utils import get_stamp

if False:  # pragma: nocover
    from django.contrib.auth.base_user import AbstractBaseUser


@pytest.fixture()
def user_model():
    """Returns user model class.

    Example::

        def test_this(user_model):
            model_cls = user_model

    """
    from django.contrib.auth import get_user_model

    return get_user_model()


@pytest.fixture()
def user_create(user_model):
    """Allows Django user object generation.

    Example::

        def test_this(user_create):
            user = user_create()

    .. note:: User password is accessible via `password_plain` attribute.

    :param bool superuser: Whether to create a superuser.
    :param bool anonymous: Whether to create an anonymous user.
    :param dict attributes: Additional user object attributes to initialize.

    """
    from django.contrib.auth.models import AnonymousUser

    def user_create_(superuser=False, anonymous=False, attributes=None):
        """
        :rtype: AbstractBaseUser
        """
        if anonymous:
            return AnonymousUser()

        attributes = attributes or {}
        manager = user_model._default_manager

        username = (('admin' if superuser else 'user') + '_' + get_stamp())

        kwargs = {
            'username': username,
            'email': '%s@example.com' % username,
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
def user(user_create):
    """Exposes Django user object.

    Shortcut for `user_create` fixture.

    Example::

        def test_this(user):
            username = user.username

    .. note:: User password is accessible via `password_plain` attribute.

    """
    return user_create()
