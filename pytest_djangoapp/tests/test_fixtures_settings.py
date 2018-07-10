
def test_settings(settings):
    from django.conf import settings as _actual_settings

    assert not _actual_settings.DEBUG

    settings.update({
        'DEBUG': True,
        'SOMENEW': 'value',
    })

    assert _actual_settings.DEBUG

    settings.SOMENEW = 'other'


def test_context_manager(settings):
    from django.conf import settings as _actual_settings

    assert not _actual_settings.DEBUG

    with settings(SOME=1, DEBUG=True):
        assert _actual_settings.SOME == 1
        assert _actual_settings.DEBUG

    assert not hasattr(_actual_settings, 'SOME')
    assert not _actual_settings.DEBUG

    assert 'django.contrib.sites' in _actual_settings.INSTALLED_APPS
    assert 'django.contrib.sessions.middleware.SessionMiddleware' in _actual_settings.MIDDLEWARE
    assert 'django.contrib.sessions.middleware.SessionMiddleware' in _actual_settings.MIDDLEWARE_CLASSES
    assert 'dummy' in _actual_settings.DATABASES
