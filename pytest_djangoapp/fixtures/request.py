import pytest

from django.http import HttpRequest


@pytest.fixture
def mock_request():
    """Fixture allowing mocked request object generation.

    Example::

        def test_this(mock_request):
            referer = 'some'
            request = mock_request(path=referer, meta={
                'HTTP_REFERER': referer
            })


    """
    def mock_request_(**kwargs):
        return MockRequest(**kwargs)

    return mock_request_


class MockRequest(HttpRequest):

    def __init__(self, path=None, user=None, meta=None):
        super(MockRequest, self).__init__()

        self.path = path or '/'
        self.user = user
        self.META = meta
