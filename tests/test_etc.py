from pytest_djangoapp import configure_djangoapp_plugin
from pytest_djangoapp.configuration import Configuration


def test_whole_project_testing(request):
    configure_djangoapp_plugin('tests.settings_project')
    settings_dict = Configuration.get_combined(request.config)
    assert '_' not in settings_dict
    assert 'SOME_ATTR' in settings_dict
    assert 'some_function' not in settings_dict
