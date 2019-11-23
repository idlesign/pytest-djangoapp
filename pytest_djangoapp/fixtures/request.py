# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from django.test import RequestFactory, Client

try:
    from django.urls import reverse

except ImportError:  # Django < 2.0
    from django.core.urlresolvers import reverse


if False:  # pragma: nocover
    from django.contrib.auth.base_user import AbstractBaseUser
    from django.http import HttpRequest


def _contribute_ajax(headers, flag):
    if flag:
        headers['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'


class DjangoappRequestFactory(RequestFactory):

    def __init__(self, ajax=False, **defaults):
        _contribute_ajax(defaults, ajax)
        super(DjangoappRequestFactory, self).__init__(**defaults)

    def generic(self, method, path, *args, **kwargs):

        if isinstance(path, tuple):
            path = reverse(path[0], kwargs=path[1])

        return super(DjangoappRequestFactory, self).generic(method, path, *args, **kwargs)


class DjagoappClient(Client, DjangoappRequestFactory):

    def __init__(self, ajax=False, user=None, enforce_csrf_checks=False, raise_exceptions=True, **defaults):
        _contribute_ajax(defaults, ajax)

        super(DjagoappClient, self).__init__(enforce_csrf_checks, **defaults)

        if user:
            assert hasattr(user, 'password_plain'), (
                'Request client expects a user created with `user` or `user_create` fixtures.')

            logged_in = self.login(username=user.username, password=user.password_plain)

        else:
            logged_in = None

        self.user = user
        self.user_logged_in = logged_in
        self._raise_exc = raise_exceptions

    def store_exc_info(self, **kwargs):
        if self._raise_exc:
            super(DjagoappClient, self).store_exc_info(**kwargs)


@pytest.fixture
def request_factory():
    """Fixture allowing request object generation.

    Example::

        def test_this(request_factory):
            factory = request_factory()

    :param kwargs:

    """
    def request_factory_(**kwargs):
        """
        :rtype: RequestFactory
        """
        return DjangoappRequestFactory(**kwargs)

    return request_factory_


@pytest.fixture
def request_get(request_factory):
    """Fixture allowing GET request object generation.

    Example::

        def test_this(request_get):
            request = request_get('/some')


    :param str|unicode path:

    :param AbstractBaseUser user: User making this request.

    :param bool ajax: Make AJAX (XMLHttpRequest) request.

    :param kwargs: Additional arguments for .get() method.

    """
    def request_get_(path=None, user=None, ajax=False, **kwargs):
        """
        :rtype: HttpRequest
        """
        path = path or '/'
        request = request_factory(ajax=ajax).get(path, **kwargs)
        if user:
            request.user = user
        return request

    return request_get_


@pytest.fixture
def request_post(request_factory):
    """Fixture allowing POST request object generation.

    Example::

        def test_this(request_post):
            request = request_post('/some', {'a': 'b'})


    :param str|unicode path:

    :param dict data: Data to post.

    :param AbstractBaseUser user: User making this request.

    :param bool ajax: Make AJAX (XMLHttpRequest) request.

    :param kwargs: Additional arguments for .post() method.

    """
    def request_post_(path=None, data=None, user=None, ajax=False, **kwargs):
        """
        :rtype: HttpRequest
        """
        path = path or '/'
        request = request_factory(ajax=ajax).post(path, data, **kwargs)
        if user:
            request.user = user
        return request

    return request_post_


@pytest.fixture
def request_client():
    """Fixture allowing test client object generation.

    Example::

        def test_this(request_client):

            client = request_client()

            response = client.get(
                ('someview', {'somearg': 'one', 'otherarg': 33})
            ).content

            ...

            ajax_client = request_client(ajax=True)
            ...


    :param bool ajax: Make AJAX (XMLHttpRequest) requests.

    :param bool raise_exceptions: Do not allow Django technical exception handlers
        to catch exceptions issued by views, propagate them instead.

    :param AbstractBaseUser user: User to perform queries from.

    :param kwargs: Additional arguments for test client initialization.

    """
    def request_client_(ajax=False, user=None, raise_exceptions=True, **kwargs):
        """
        :rtype: DjagoappClient
        """
        return DjagoappClient(ajax=ajax, user=user, raise_exceptions=raise_exceptions, **kwargs)

    return request_client_
