import pytest

def test_settings(settings):
    from django.conf import settings as _actual_settings

    assert not _actual_settings.DEBUG

    settings.update({
        'DEBUG': True,
        'SOMENEW': 'value',
    })

    assert settings.DEBUG
    assert settings.SOMENEW == 'value'

    assert _actual_settings.DEBUG
    assert _actual_settings.SOMENEW == 'value'

    settings.SOMENEW = 'other'

    assert settings.SOMENEW == 'other'

    assert _actual_settings.SOMENEW == 'other'


def test_context_manager(settings):
    from django.conf import settings as _actual_settings

    assert not _actual_settings.DEBUG

    with settings(SOME=1, DEBUG=True):
        assert settings.SOME == 1
        assert settings.DEBUG

        assert _actual_settings.SOME == 1
        assert _actual_settings.DEBUG

        settings.OTHER = 1
        assert settings.OTHER == 1
        assert _actual_settings.OTHER == 1

    assert not hasattr(settings, 'SOME')
    assert not hasattr(settings, 'OTHER')

    assert not _actual_settings.DEBUG
    assert not hasattr(_actual_settings, 'SOME')
    assert not hasattr(_actual_settings, 'OTHER')

    assert 'django.contrib.sites' in _actual_settings.INSTALLED_APPS
    assert 'django.contrib.sessions.middleware.SessionMiddleware' in _actual_settings.MIDDLEWARE
    assert 'django.contrib.sessions.middleware.SessionMiddleware' in _actual_settings.MIDDLEWARE_CLASSES
    assert 'dummy' in _actual_settings.DATABASES

    settings.DEBUG = False

    assert not _actual_settings.DEBUG

    settings.SOME = 2

    assert settings.SOME == 2

    assert _actual_settings.SOME == 2

    with settings(SOME='value', DEBUG=True):
        assert settings.SOME == 'value'
        assert settings.DEBUG

        assert _actual_settings.SOME == 'value'
        assert _actual_settings.DEBUG

    assert not settings.DEBUG
    assert not _actual_settings.DEBUG

    # SOME from before the context manager is now removed.
    assert not hasattr(settings, 'SOME')
    assert not hasattr(_actual_settings, 'SOME')

    with settings:
        settings.OTHER = 1
        assert settings.OTHER == 1
        assert _actual_settings.OTHER == 1

    assert not _actual_settings.DEBUG

    assert not hasattr(settings, 'SOME')
    assert not hasattr(settings, 'OTHER')

    assert not hasattr(_actual_settings, 'SOME')
    assert not hasattr(_actual_settings, 'OTHER')

    settings.OTHER = 1
    assert settings.OTHER == 1
