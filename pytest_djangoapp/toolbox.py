# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from .configuration import Configuration


def configure_djangoapp_plugin(
        settings=None, app_name=None, admin_contrib=False, settings_hook=None, migrate=True, **kwargs):
    """Configures djangoapp pytest plugin.

    :param dict settings: Django project settings to override defaults.

    :param str|unicode app_name: Name of your application you write tests for.
        If not set ``djangoapp`` will try to guess (``tests`` dir needs to be inside application directory).

    :param bool admin_contrib: Setup Django to test Admin contrib related parts.

    :param callable settings_hook: Allows setting a function to get resulting settings.

        Function must accept settings dictionary, and return resulting settings dictionary.

        .. code-block:: python

            def hook_func(settings):
                return settings

    :param bool migrate: Allows applying or skipping migration applying process. 
        Skipping could be useful for testing applications with many migrations.

    :param kwargs: Additional arguments.

        Use `extend_` prefix to extend default configuration.

        .. code:: python

            configure_djangoapp_plugin(

                extend_INSTALLED_APPS=[
                    'django.contrib.auth',
                    'django.contrib.contenttypes',
                    'django.contrib.sessions'
                ],
                extend_DATABASES={
                    'dummy': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': ':memory:',
                    },
                },
            )

    :returns: Plugin name to add into ``pytest_plugins`` module attribute of ``conftest.py``.

    :rtype: str

    """
    try:
        import django

    except ImportError:  # pragma: nocover
        raise Exception('Django is no available in test environment.')

    Configuration.set(
        settings_dict=settings,
        app_name=app_name,
        admin_contrib=admin_contrib,
        settings_hook=settings_hook,
        migrate=migrate,
        **kwargs)

    return str('pytest_djangoapp.plugin')
