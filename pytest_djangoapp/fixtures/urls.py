import sys

from django.urls import include, path

import pytest

from pytest_djangoapp.configuration import Configuration

from . import djapp_options, settings


@pytest.fixture(scope="session")
def fake_global_urlconf_module():
    def fake_module(name):
        module = type(sys)(name)
        sys.modules[name] = module
        return module

    name = '_urls'

    urlconf = sys.modules.get(name)
    if not urlconf:
        urlconf = fake_module(name)
        urlconf.urlpatterns = []

    yield urlconf


@pytest.fixture(scope="session")
def fake_global_urlpatterns(fake_global_urlconf_module):
    yield fake_global_urlconf_module.urlpatterns


@pytest.fixture()
def urlpatterns(settings, fake_global_urlconf_module):

    with settings(ROOT_URLCONF=fake_global_urlconf_module.__name__):
        yield fake_global_urlconf_module.urlpatterns


@pytest.fixture()
def inject_app_urls(urlpatterns, app_name):
    urls_module = '{}.urls'.format(app_name)

    if any(urlpattern.urlconf_module.__name__ == urls_module for urlpattern in urlpatterns):
        return

    urlpatterns.append(path('', include(urls_module)))


@pytest.fixture()
def inject_testapp_urls(urlpatterns):
    testapp_name = Configuration.DIR_TESTAPP
    urls_module = '{}.urls'.format(testapp_name)

    if any(urlpattern.urlconf_module.__name__ == urls_module for urlpattern in urlpatterns):
        return

    urlpatterns.append(path('', include(urls_module)))
