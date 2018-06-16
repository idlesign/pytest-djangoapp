# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from .configuration import Configuration


def configure_djangoapp_plugin(settings=None, app_name=None):
    """Configurates djangoapp pytest plugin.

    :param dict settings: Django project settings to override defaults.

    :param str|unicode app_name: Name of your application you write tests for.
        If not set ``djangoapp`` will try to guess (``tests`` dir needs to be inside application directory).

    :returns: Plugin name to add into ``pytest_plugins`` module attribute of ``conftest.py``.
    :rtype: str

    """
    try:
        import django

    except ImportError:  # pragma: nocover
        raise Exception('Django is no available in test environment.')

    Configuration.set(settings_dict=settings, app_name=app_name)

    return str('pytest_djangoapp.plugin')
