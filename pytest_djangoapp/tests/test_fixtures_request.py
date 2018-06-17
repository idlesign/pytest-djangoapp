try:
    from django.urls import reverse

except ImportError:  # Django<2.0
    from django.core.urlresolvers import reverse


def test_request_factory(request_factory):
    assert request_factory()


def test_request_get(request_get, user_create):
    assert request_get(user=user_create())


def test_request_post(request_post, user_create):
    assert request_post(data={'a': 'b'}, user=user_create())


def test_request_client(request_client):
    client = request_client()
    assert client

    response = client.get(reverse('index'))

    assert response.status_code == 200
