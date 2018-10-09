import pytest
import sys


@pytest.mark.skipif(sys.version_info > (2, 0), reason='teardown without setup should pass')
def test_teardown_without_setup():
    assert True
