def test_request_factory(request_factory):
    assert request_factory()


def test_request_get(request_get, user_create):
    assert request_get(user=user_create())
    assert request_get(ajax=True)


def test_request_post(request_post, user_create):
    assert request_post(data={'a': 'b'}, user=user_create())
    assert request_post(ajax=True, data={'a': 'b'})


def test_request_client(request_client, user_create):
    client = request_client()
    assert client
    assert client.user is None
    assert not client.user_logged_in

    response = client.get(('index', {'some_id': 10}))

    assert response.status_code == 200
    assert response.content == b'10 | fine /static/blank.png'

    # Now AJAX client.
    client = request_client(ajax=True)

    response = client.get(('index', {'some_id': 22}))

    assert response.status_code == 200
    assert b'ajaxed' in response.content

    new_user = user_create()
    client = request_client(user=new_user)

    assert client.user is new_user
    assert client.user_logged_in

    # now technical 500 view
    client = request_client(raise_exceptions=False)
    response = client.get('/raiser/')
    assert b'<h1>Server Error (500)</h1>' in response.content

    # now json
    client = request_client(json=True)
    response = client.post(('index', {'some_id': 10}), {'a': 'b'})
    content = response.content
    assert b'json' in content
