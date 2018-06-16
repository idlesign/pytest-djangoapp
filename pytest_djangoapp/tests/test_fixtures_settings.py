
def test_settings(settings):
    from django.conf import settings as _actual_settings

    assert not _actual_settings.DEBUG

    settings.update({
        'DEBUG': True,
        'SOMENEW': 'value',
    })

    assert _actual_settings.DEBUG

    settings.SOMENEW = 'other'
