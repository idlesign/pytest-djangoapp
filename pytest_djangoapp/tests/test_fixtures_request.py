
def test_request_factory(request_factory):
    assert request_factory()


def test_request_get(request_get, user_create):
    assert request_get(user=user_create())
