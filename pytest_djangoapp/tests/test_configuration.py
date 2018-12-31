import pytest

from pytest_djangoapp.configuration import Configuration


def test_configration(pytestconfig):

    settings = Configuration.get()
    settings[Configuration._KEY_APP] = 'some'

    assert Configuration.get_combined(pytestconfig)

    settings[Configuration._KEY_APP] = ''
    assert Configuration.get_combined(pytestconfig)

    def swap_dir(level):

        old_dir = pytestconfig.invocation_dir

        try:
            pytestconfig.invocation_dir = old_dir.parts()[level]
            assert Configuration.get_combined(pytestconfig)

        finally:
            pytestconfig.invocation_dir = old_dir

    with pytest.raises(Exception):
        # Unable to deduce app name.
        swap_dir(-4)


def test_settings_hook():
    from django.conf import settings
    assert settings.HOOKED
