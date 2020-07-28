# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import pytest
from django.conf import settings as django_settings

from pytest_djangoapp.configuration import Configuration

_UNSET = set()


def _run_settings_hook(djapp_options, settings):
    hook = djapp_options[Configuration._KEY_HOOK] or (lambda settings_dict: settings_dict)
    return hook(settings)


def _merge(settings):
    merged = {}
    for setting in dir(django_settings):
        if setting.isupper():
            merged[setting] = getattr(django_settings, setting)

    for setting in dir(settings):
        if setting.isupper():
            merged[setting] = getattr(settings, setting)

    return merged


@pytest.fixture()
def settings():
    """Fixture allowing to temporarily override project settings.

    Example::

        def test_this(settings):
            # By one.
            settings.DEBUG = True

            # Batch.
            settings.update({
                'DEBUG': True,
                'ROOT_URLCONF': 'module.urls',
            })

            # Context manager.
            with settings(DEBUG=True):
                ...


    :rtype: SettingsProxy
    """
    djapp_options = Configuration.get()[Configuration._prefix]
    proxy = SettingsProxy(djapp_options)

    yield proxy

    proxy.restore_initial()


class SettingsProxy(object):

    def __init__(self, djapp_options):
        self._options = djapp_options
        self._settings = django_settings
        self._overridden = {}

    def __setattr__(self, name, value):

        if name in {'_options', '_settings', '_overridden'}:
            return super(SettingsProxy, self).__setattr__(name, value)

        self._set(name, value)

    def __call__(self, **kwargs):
        # Aid context manager mode.
        do_set = self._set

        for key, val in kwargs.items():
            do_set(key, val)

        self.update(_run_settings_hook(self._options, _merge(self._settings)))

        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore_initial()
        self.update(_run_settings_hook(self._options, _merge(self._settings)))

    def _set(self, name, value):
        settings = self._settings
        overridden = self._overridden

        current_val = getattr(settings, name, _UNSET)

        if name not in overridden:
            # Handle subsequent changes.
            overridden[name] = current_val

        setattr(settings, name, value)

    def update(self, settings):
        """Mass update settings.

        :param dict settings:
        """
        for name, value in settings.items():
            self._set(name, value)

    def restore_initial(self):
        """Restore initial settings."""

        settings = self._settings
        unset = _UNSET

        for key, val in self._overridden.items():
            if val is unset:
                # wipe
                delattr(settings, key)

            else:
                # restore
                setattr(settings, key, val)
