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
    """Returns function allowing creation of Django user.

    Example::

        def test_this(user_create):
            user = user_create()

    """
    from django.contrib.auth.models import AnonymousUser

    def user_create_(superuser=False, anonymous=False, attributes=None):
        """Create user.

        :param bool superuser: Whether to create superuser.
        :param bool anonymous: Whether to create anonymous user.
        :param dict attributes: Additional user attributes to initialize.

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

        return user

    return user_create_

