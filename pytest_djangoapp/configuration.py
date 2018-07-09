# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from threading import local

_THREAD_LOCAL = local()
setattr(_THREAD_LOCAL, 'configuration', {})


class Configuration(object):

    _prefix = 'DJANGOAPP_'
    _KEY_APP = _prefix +'APP_NAME'
    _KEY_EXTEND = _prefix + 'DJANGOAPP_EXTEND'

    DIR_TESTAPP = 'testapp'
    """Name of test application directory.
    
    Test application directory should be placed inside `tests` directory 
    and needs to be a Python package (contain __init__.py).
     
    Test application is useful to place there modules like `urls.py`,
    `models.py` (e.g. with custom models), etc.
    
    """

    @classmethod
    def get(cls):
        return _THREAD_LOCAL.configuration

    @classmethod
    def set(cls, settings_dict=None, app_name=None, **kwargs):
        """
        :param dict settings_dict:

        :param str|unicode app_name:

        :param kwargs: Additional arguments.

            Use `extend_` prefix to extend default configuration.
            E.g.: extend_INSTALLED_APPS=['a']

        """
        settings_dict = settings_dict or {}

        extend = {}

        for key, val in kwargs.items():
            _, _, extend_key = key.partition('extend_')

            if extend_key and extend_key == extend_key.upper():
                extend[extend_key] = val

        base_settings = {
            cls._KEY_APP: app_name,
            cls._KEY_EXTEND: extend,
        }
        base_settings.update(settings_dict)

        _THREAD_LOCAL.configuration = base_settings

    @classmethod
    def get_defaults(cls):
        """
        :rtype: dict
        """
        from django.conf import global_settings

        if hasattr(global_settings, 'MIDDLEWARE_CLASSES'):
            middleware = global_settings.MIDDLEWARE_CLASSES

        else:
            middleware = global_settings.MIDDLEWARE

        installed_apps = list(global_settings.INSTALLED_APPS[:])
        installed_apps.extend([
            'django.contrib.auth',
            'django.contrib.contenttypes',
        ])
        installed_apps = list(set(installed_apps))

        settings_dict = dict(

            ALLOWED_HOSTS=(
                global_settings.ALLOWED_HOSTS +
                # Satisfy Django test client needed in Django < 2.0
                ['testserver']
            ),

            INSTALLED_APPS=installed_apps,
            STATIC_URL='/static/',

            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                },
            },

            MIDDLEWARE=middleware,
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

        for key, value in defaults[cls._KEY_EXTEND].items():
            default_value = defaults.get(key, [])

            if isinstance(default_value, (list, tuple)):
                extended = default_value

                if not isinstance(default_value, list):
                    # We don't need list copying, since
                    # we want to MIDDLEWARE/MIDDLEWARE_CLASSES
                    # and similar lists to be extended inplace.
                    extended = list(default_value)

                extended.extend(value)
                defaults[key] = extended

            elif isinstance(default_value, dict):
                defaults[key].update(value)

            else:  # pragma: nocover
                raise ValueError('Unable to extend `%s` option.' % key)

        installed_apps = defaults['INSTALLED_APPS']

        if app_name:

            if app_name not in installed_apps:
                installed_apps.append(app_name)

        else:
            dir_current = pytest_config.invocation_dir
            dir_tests = None

            app_name = dir_current.basename

            if app_name == 'tests':
                # Support certain module or function invocation tests dir as base (e.g. PyCharm behaviour).
                app_name = dir_current.parts()[-2].basename
                dir_tests = dir_current

            try:
                dir_tests = dir_current.listdir('tests')[0]

            except IndexError:
                pass

            if not dir_tests:
                # No `tests` subdir found. Let's to try to deduce.

                app_name = None

                from setuptools import find_packages
                import py

                candidate_latest = ''
                candidates = []

                for package in find_packages('%s' % dir_current):
                    # Consider only top level packages.
                    if not candidate_latest or not package.startswith(candidate_latest):
                        candidates.append(package)
                        candidate_latest = package

                for candidate in candidates:
                    dirs = py.path.local(candidate).listdir('tests')

                    if dirs:
                        app_name = candidate
                        dir_tests = dirs[0]
                        break

            if not app_name:
                raise Exception(
                    'Unable to deduce application name. '
                    'Check application package and `tests` directory exists. '
                    'Current dir: %s' % dir_current)

            installed_apps.append(app_name)

            if dir_tests:
                # Try to find and add an additional test app.
                dir_testapp_name = cls.DIR_TESTAPP
                dir_testapp = dir_tests.listdir(dir_testapp_name)

                if dir_testapp:
                    dir_testapp = dir_testapp[0]

                    testapp_name = '%s.tests.%s' % (app_name, dir_testapp_name)

                    installed_apps.append(testapp_name)

                    if dir_testapp.listdir('urls.py'):
                        # Set customized `urls.py`.
                        defaults['ROOT_URLCONF'] = '%s.urls' % testapp_name

        return defaults
