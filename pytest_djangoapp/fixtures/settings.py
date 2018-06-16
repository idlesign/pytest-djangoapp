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


    :rtype: SettingsProxy
    """
    proxy = SettingsProxy()

    yield proxy

    proxy.restore_initial()


class SettingsProxy(object):

    __slots__ = ['_settings', '_overridden']

    def __init__(self):
        self._settings = django_settings
        self._overridden = {}

    def __setattr__(self, name, value):

        if name in self.__slots__:
            return super(SettingsProxy, self).__setattr__(name, value)

        self._set(name, value)

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
