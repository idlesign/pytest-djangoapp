# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from django.test import RequestFactory, Client

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


class DjagoappClient(Client):

    def __init__(self, ajax=False, enforce_csrf_checks=False, **defaults):
        _contribute_ajax(defaults, ajax)
        super(DjagoappClient, self).__init__(enforce_csrf_checks, **defaults)


@pytest.fixture
def request_factory():
    """Fixture allowing request object generation.

    Example::

        def test_this(request_factory):
            factory = request_factory()

    :param kwargs:
    :rtype: RequestFactory

    """
    def request_factory_(**kwargs):
        """
        :param kwargs:
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

    :rtype: HttpRequest

    """
    def request_get_(path=None, user=None, ajax=False, **kwargs):
        """
        :param str|unicode path:

        :param AbstractBaseUser user: User making this request.

        :param bool ajax: Make AJAX (XMLHttpRequest) request.

        :param kwargs: Additional arguments for .get() method.

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

    :rtype: HttpRequest

    """
    def request_post_(path=None, data=None, user=None, ajax=False, **kwargs):
        """
        :param str|unicode path:

        :param dict data: Data to post.

        :param AbstractBaseUser user: User making this request.

        :param bool ajax: Make AJAX (XMLHttpRequest) request.

        :param kwargs: Additional arguments for .post() method.

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
            ...

            ajax_client = request_client(ajax=True)
            ...


    :param bool ajax: Make AJAX (XMLHttpRequest) requests.

    :param kwargs: Additional arguments for test client initialization.

    :rtype: DjagoappClient

    """
    def request_client_(ajax=False, **kwargs):
        """
        :param bool ajax: Make AJAX (XMLHttpRequest) requests.

        :param kwargs: Additional arguments for test client initialization.

        :rtype: DjagoappClient
        """
        return DjagoappClient(ajax=ajax, **kwargs)

    return request_client_
