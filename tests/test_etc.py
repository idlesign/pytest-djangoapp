import sys

import pytest

from pytest_djangoapp import configure_djangoapp_plugin
from pytest_djangoapp.configuration import Configuration


@pytest.mark.skipif(sys.version_info > (2, 0), reason='teardown without setup should pass')
def test_teardown_without_setup():
    assert True


@pytest.mark.skipif(sys.version_info < (3, 0), reason='whole project test are for Py 3')
def test_whole_project_testing(request):
    configure_djangoapp_plugin('pytest_djangoapp.tests.settings_project')
    settings_dict = Configuration.get_combined(request.config)
    assert '_' not in settings_dict
    assert 'SOME_ATTR' in settings_dict
    assert 'some_function' not in settings_dict
