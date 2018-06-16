
from pytest_djangoapp.configuration import Configuration


def test_configration(pytestconfig):
    settings = Configuration.get()
    settings[Configuration._KEY_APP] = ''
    assert Configuration.get_combined(pytestconfig)
