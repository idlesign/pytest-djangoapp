try:
    from django.urls import reverse

except ImportError:  # Django<2.0
    from django.core.urlresolvers import reverse


def test_request_factory(request_factory):
    assert request_factory()


def test_request_get(request_get, user_create):
    assert request_get(user=user_create())
    assert request_get(ajax=True)


def test_request_post(request_post, user_create):
    assert request_post(data={'a': 'b'}, user=user_create())
    assert request_post(ajax=True, data={'a': 'b'})


def test_request_client(request_client):
    client = request_client()
    assert client

    response = client.get(reverse('index'))

    assert response.status_code == 200
    assert b'fine' in response.content

    # Now AJAX client.
    client = request_client(ajax=True)

    response = client.get(reverse('index'))

    assert response.status_code == 200
    assert b'ajaxed' in response.content
