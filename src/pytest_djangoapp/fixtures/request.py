import pytest
from django.test import RequestFactory, Client

try:
    from django.urls import reverse

except ImportError:  # Django < 2.0
    from django.core.urlresolvers import reverse


if False:  # pragma: nocover
    from django.contrib.auth.models import AbstractUser  # noqa
    from django.http import HttpRequest


def _contribute_ajax(headers, flag):
    if flag:
        headers['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'


class DjangoappRequestFactory(RequestFactory):

    def __init__(self, ajax=False, json=False, **defaults):
        _contribute_ajax(defaults, ajax)
        super(DjangoappRequestFactory, self).__init__(**defaults)
        self._json = json

    def _encode_json(self, data, content_type):
        if self._json:
            content_type = 'application/json'
        return super(DjangoappRequestFactory, self)._encode_json(data, content_type)

    def _encode_data(self, data, content_type):
        if self._json:
            content_type = 'application/json'
        return super(DjangoappRequestFactory, self)._encode_data(data, content_type)

    def generic(self, method, path, *args, **kwargs):

        if isinstance(path, tuple):
            path = reverse(path[0], kwargs=path[1])

        return super(DjangoappRequestFactory, self).generic(method, path, *args, **kwargs)


class DjagoappClient(Client, DjangoappRequestFactory):

    def __init__(
            self,
            *,
            ajax: bool = False,
            user: 'AbstractUser' = None,
            enforce_csrf_checks: bool = False,
            raise_exceptions: bool = True,
            json: bool = False,
            **defaults
    ):
        _contribute_ajax(defaults, ajax)

        super(DjagoappClient, self).__init__(enforce_csrf_checks, json=json, **defaults)

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

    ```py
    def test_this(request_factory):
        factory = request_factory()
    ```

    :param kwargs:

    """
    def request_factory_(**kwargs) -> DjangoappRequestFactory:
        return DjangoappRequestFactory(**kwargs)

    return request_factory_


@pytest.fixture
def request_get(request_factory):
    """Fixture allowing GET request object generation.

    ```py
    def test_this(request_get):
        request = request_get('/some')
    ```

    :param path:

    :param user: User making this request.

    :param ajax: Make AJAX (XMLHttpRequest) request.

    :param kwargs: Additional arguments for .get() method.

    """
    def request_get_(path: str = None, *, user: 'AbstractUser' = None, ajax: bool = False, **kwargs) -> 'HttpRequest':

        path = path or '/'
        request = request_factory(ajax=ajax).get(path, **kwargs)
        if user:
            request.user = user
        return request

    return request_get_


@pytest.fixture
def request_post(request_factory):
    """Fixture allowing POST request object generation.

    ```py
    def test_this(request_post):
        request = request_post('/some', {'a': 'b'})
    ```

    :param path:

    :param data: Data to post.

    :param user: User making this request.

    :param ajax: Make AJAX (XMLHttpRequest) request.

    :param kwargs: Additional arguments for .post() method.

    """
    def request_post_(
        path: str = None,
        data: dict = None,
        *,
        user: 'AbstractUser' = None,
        ajax: bool = False,
        **kwargs
    ) -> 'HttpRequest':

        path = path or '/'
        request = request_factory(ajax=ajax).post(path, data, **kwargs)
        if user:
            request.user = user
        return request

    return request_post_


@pytest.fixture
def request_client():
    """Fixture allowing test client object generation.

    ```py
    def test_this(request_client):

        client = request_client()

        response = client.get(
            ('someview', {'somearg': 'one', 'otherarg': 33})
        ).content

        ...

        ajax_client = request_client(ajax=True)
        ...
    ```

    :param ajax: Make AJAX (XMLHttpRequest) requests.

    :param user: User to perform queries from.

    :param raise_exceptions: Do not allow Django technical exception handlers
        to catch exceptions issued by views, propagate them instead.

    :param json: Encode data as JSON.

        .. warning:: To be used with Django 2.1+

    :param kwargs: Additional arguments for test client initialization.

    """
    def request_client_(
        *,
        ajax: bool = False,
        user: 'AbstractUser' = None,
        raise_exceptions: bool = True,
        json: bool = False,
        **kwargs
    ) -> DjagoappClient:

        return DjagoappClient(
            ajax=ajax,
            user=user,
            raise_exceptions=raise_exceptions,
            json=json,
            **kwargs
        )

    return request_client_
