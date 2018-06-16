# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from threading import local

_THREAD_LOCAL = local()
setattr(_THREAD_LOCAL, 'configuration', {})


class Configuration(object):

    _KEY_APP = 'DJANGOAPP_APP_NAME'

    @classmethod
    def get(cls):
        return _THREAD_LOCAL.configuration

    @classmethod
    def set(cls, settings_dict=None, app_name=None):
        """
        :param dict settings_dict:
        :param str|unicode app_name:
        """
        settings_dict = settings_dict or {}

        base_settings = {
            cls._KEY_APP: app_name,
        }
        base_settings.update(settings_dict)

        _THREAD_LOCAL.configuration = base_settings

    @classmethod
    def get_defaults(cls):
        """
        :rtype: dict
        """
        from django.conf import global_settings

        if hasattr(global_settings, 'MIDDLEWARE'):
            middleware = global_settings.MIDDLEWARE

        else:
            middleware = global_settings.MIDDLEWARE_CLASSES

        installed_apps = list(global_settings.INSTALLED_APPS[:])
        installed_apps.extend([
            'django.contrib.auth',
            'django.contrib.contenttypes',
        ])
        installed_apps = list(set(installed_apps))

        settings_dict = dict(

            INSTALLED_APPS=installed_apps,

            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                },
            },

            MIDDLEWARE_CLASSES=middleware,  # Prevents Django 1.7 warning.

            TEMPLATES=[
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'APP_DIRS': True,
                },
            ],

        )

        try:
            # Django < 1.8
            settings_dict['TEMPLATE_CONTEXT_PROCESSORS'] = tuple(global_settings.TEMPLATE_CONTEXT_PROCESSORS) + (
                'django.core.context_processors.request',
            )

        except AttributeError:
            pass

        return settings_dict.copy()

    @classmethod
    def get_combined(cls, pytest_config):
        """
        :rtype: dict
        """
        settings = cls.get()

        defaults = cls.get_defaults()
        defaults.update(settings)

        app_name = defaults[cls._KEY_APP]

        installed_apps = defaults['INSTALLED_APPS']

        if app_name:

            if app_name not in installed_apps:
                installed_apps.append(app_name)

        else:
            app_name = pytest_config.invocation_dir.basename

            if app_name == 'tests':
                # Support certain module or function invocation tests dir as base (e.g. PyCharm behaviour).
                app_name = pytest_config.invocation_dir.parts()[-2].basename

            # todo tests dir + urlconf
            installed_apps.extend([
                app_name,
                '%s.tests' % app_name,
            ])
            defaults['ROOT_URLCONF'] = '%s.tests.urls' % app_name

        return defaults
