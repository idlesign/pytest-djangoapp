import pytest

from django.test import RequestFactory

if False:  # pragma: nocover
    from django.contrib.auth.base_user import AbstractBaseUser
    from django.http import HttpRequest


@pytest.fixture
def request_factory():
    """Fixture allowing request object generation.

    Example::

        def test_this(request_factory):
            factory = request_factory()


    """
    def request_factory_(**kwargs):
        """
        :param kwargs:
        :rtype: RequestFactory
        """
        return RequestFactory(**kwargs)

    return request_factory_


@pytest.fixture
def request_get(request_factory):
    """Fixture allowing GET request object generation.

    Example::

        def test_this(request_get):
            request = request_get('/some')


    """
    def request_get_(path=None, user=None, **kwargs):
        """
        :param str|unicode path:
        :param AbstractBaseUser user:
        :param kwargs:
        :rtype: HttpRequest
        """
        path = path or '/'
        request = request_factory().get(path, **kwargs)
        if user:
            request.user = user
        return request

    return request_get_
