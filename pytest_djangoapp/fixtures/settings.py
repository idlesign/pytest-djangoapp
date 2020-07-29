# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import pytest
from django.conf import settings as django_settings


_UNSET = set()


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
    proxy = SettingsProxy()

    yield proxy

    proxy.restore_initial()


_PROXY_SETTING_ATTRS = '_settings', '_overridden'


class SettingsProxy(object):

    def __init__(self):
        self._settings = django_settings
        self._overridden = {}

    def __setattr__(self, name, value):

        if name in _PROXY_SETTING_ATTRS:
            return super(SettingsProxy, self).__setattr__(name, value)

        self._set(name, value)

    def __getattr__(self, name):

        if name in _PROXY_SETTING_ATTRS:
            return super(SettingsProxy, self).__getattr__(name)

        try:
            return getattr(self._overridden, name)
        except AttributeError:
            return getattr(self._settings, name)

    def __call__(self, **kwargs):
        # Aid context manager mode.
        do_set = self._set

        for key, val in kwargs.items():
            do_set(key, val)

        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore_initial()

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
