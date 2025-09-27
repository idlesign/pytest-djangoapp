from __future__ import annotations

from threading import local
from typing import TYPE_CHECKING, Callable

from pytest_djangoapp.exceptions import DjangoappException

if TYPE_CHECKING:
    from py.path import LocalPath

_THREAD_LOCAL = local()
_THREAD_LOCAL.configuration = {}


class FakeMigrationModules:
    """Allows skipping migration applying process."""

    def __init__(self, module_name: str):
        self.module_name = module_name

    def __getitem__(self, item: str) -> str:
        return self.module_name

    def __contains__(self, item: str):
        return True


class Configuration:
    _prefix = 'DJANGOAPP_OPTIONS'
    _KEY_ADMIN = 'admin'
    KEY_APP = 'app_name'
    _KEY_EXTEND = 'extend'
    _KEY_HOOK = 'hook'
    _KEY_MIGRATE = 'migrate'

    DIR_TESTAPP = 'testapp'
    """Name of test application directory.

    Test application directory should be placed inside `tests` directory 
    and needs to be a Python package (contain __init__.py).

    Test application is useful to place there modules like `urls.py`,
    `models.py` (e.g. with custom models), etc.

    """

    @classmethod
    def get(cls) -> dict:
        return _THREAD_LOCAL.configuration

    @classmethod
    def set(
            cls,
            settings_dict: str | dict | None = None,
            *,
            app_name: str | None = None,
            admin_contrib: bool = False,
            settings_hook: Callable | None = None,
            migrate: bool = True,
            **kwargs
    ):
        """
        :param settings_dict:

        :param app_name:

        :param admin_contrib: Setup Django to test Admin contrib related parts.

        :param settings_hook: Allows setting a function to get resulting settings.

            Function must accept settings dictionary, and return resulting settings dictionary.

            .. code-block:: python

                def hook_func(settings):
                    return settings

        :param migrate: Allows applying or skipping migration applying process.
            Skipping could be useful for testing applications with many migrations.

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
            cls._prefix: {
                cls.KEY_APP: app_name,
                cls._KEY_EXTEND: extend,
                cls._KEY_ADMIN: admin_contrib,
                cls._KEY_HOOK: settings_hook,
                cls._KEY_MIGRATE: migrate,
            }
        }

        base_settings.update(settings_dict)

        _THREAD_LOCAL.configuration = base_settings

    @classmethod
    def _extend(cls, container: list[str], new: list[str]):
        for item in new:
            if item not in container:
                container.append(item)

    @classmethod
    def get_defaults(cls) -> dict:
        from django.conf import global_settings

        if hasattr(global_settings, 'MIDDLEWARE_CLASSES'):
            middleware = global_settings.MIDDLEWARE_CLASSES

        else:
            middleware = global_settings.MIDDLEWARE

        installed_apps = list(global_settings.INSTALLED_APPS[:])
        cls._extend(installed_apps, [
            'django.contrib.auth',
            'django.contrib.contenttypes',
        ])

        settings_dict = {

            'SECRET_KEY': 'djangoapp',

            'ALLOWED_HOSTS': [
                *global_settings.ALLOWED_HOSTS,
                # testserver Satisfy Django test client needed in Django < 2.0
                *['testserver', '127.0.0.1', 'localhost']
            ],

            'INSTALLED_APPS': installed_apps,
            'STATIC_URL': '/static/',

            'DATABASES': {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                },
            },

            'MIDDLEWARE': middleware,

            'EMAIL_BACKEND': 'django.core.mail.backends.locmem.EmailBackend',

            'TEMPLATES': [
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'APP_DIRS': True,
                    'OPTIONS': {'context_processors': ['django.contrib.messages.context_processors.messages']}
                },
            ],

        }

        return settings_dict.copy()

    @classmethod
    def _get_src_subdir(cls, dir_target: LocalPath) -> LocalPath | None:
        dir_src = dir_target / 'src'
        return dir_src if dir_src.exists() else None

    @classmethod
    def _find_package_dirs(cls, target_dir: LocalPath) -> list[LocalPath]:
        packages_dirs: list[str] = [
            obj
            for obj in target_dir.listdir()
            if obj.isdir() and (obj / '__init__.py').exists() and obj.basename != 'tests'
        ]
        return packages_dirs

    @classmethod
    def deduce_apps(
            cls,
            *,
            dir_current: LocalPath,
            project_mode: bool = False
    ) -> tuple[str, tuple[LocalPath | None, str]]:
        # We try to support
        #   * classic django tests:
        #     app/
        #     - tests/
        #   * separate tests:
        #     app/
        #     tests/
        # and both the above with `src` layout and without it
        # and run from `tests` directory and from `root`.
        dir_tests = []
        dir_app = dir_current
        app_name = dir_current.basename

        def get_app(in_dir):
            nonlocal app_name, dir_app
            if packages_dirs := cls._find_package_dirs(target_dir=in_dir):
                dir_app = packages_dirs[-1]
                app_name = dir_app.basename

        dir_target = dir_current

        if app_name == 'tests':
            # Run with `tests` as current working directory (e.g. from IDE).
            dir_parent = dir_current.parts()[-2]
            dir_tests = [dir_current]
            app_name = dir_parent.basename
            if src_subdir := cls._get_src_subdir(dir_parent):
                dir_target = src_subdir
            else:
                dir_target = dir_parent

        else:
            # Presumably run from project directory.
            if (dir_tests_ := (dir_current / 'tests')).exists():
                dir_tests = [dir_tests_]

            if src_subdir := cls._get_src_subdir(dir_target):
                dir_target = src_subdir

        get_app(dir_target)

        if not (dir_app / '__init__.py').exists() and not project_mode:
            raise DjangoappException(
                'Unable to deduce application name. '
                'Check application package and `tests` directory exists. '
                f'Current dir: {dir_current}') from None

        dir_tests = dir_tests or dir_app.listdir('tests')

        # Try to find and an additional test app.
        testapp_dir = None
        testapp_name = ''

        if dir_tests and (testapp_dirs := dir_tests[0].listdir(cls.DIR_TESTAPP)):
            testapp_dir = testapp_dirs[0]
            # three levels deep max
            depth = 3 if f'{testapp_dir}'.startswith(f'{dir_app}') else 2
            testapp_name = '.'.join(chunk.basename for chunk in testapp_dir.parts()[-depth:])

        return app_name, (testapp_dir, testapp_name)

    @classmethod
    def setup_migrations(cls, defaults: dict):

        if not defaults[cls._prefix][cls._KEY_MIGRATE]:
            from django import VERSION

            module_name = None

            if VERSION <= (1, 10):
                module_name = 'dummy_migrations'
                defaults['MIGRATIONS_MODULE_NAME'] = module_name

            defaults['MIGRATION_MODULES'] = FakeMigrationModules(module_name)

    @classmethod
    def setup_admin(cls, defaults: dict):
        extensions = defaults[cls._prefix][cls._KEY_EXTEND]

        middleware = extensions.setdefault('MIDDLEWARE', [])
        cls._extend(middleware, [
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ])
        apps = extensions.setdefault('INSTALLED_APPS', [])
        cls._extend(apps, [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.messages',
            'django.contrib.sessions',
        ])
        if templates := defaults.setdefault('TEMPLATES', []):
            processors = templates[0]['OPTIONS'].setdefault('context_processors', [])
            cls._extend(processors, [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ])

    @classmethod
    def setup_extensions(cls, defaults: dict):

        for key, value in defaults[cls._prefix][cls._KEY_EXTEND].items():
            default_value = defaults.get(key, [])

            if isinstance(default_value, (list, tuple)):
                extended = list(default_value)

                for item in value:
                    if item not in extended:
                        extended.append(item)

                defaults[key] = extended

                if key == 'MIDDLEWARE':
                    # Special case for renamed.
                    defaults['MIDDLEWARE_CLASSES'] = extended

            elif isinstance(default_value, dict):
                defaults[key].update(value)

            else:  # pragma: nocover
                raise ValueError(f'Unable to extend `{key}` option.')

    @classmethod
    def get_combined(cls, pytest_config) -> dict:
        settings = cls.get()

        defaults = cls.get_defaults()
        defaults.update(settings)

        djapp_options = defaults[cls._prefix]

        cls.setup_migrations(defaults)

        if djapp_options[cls._KEY_ADMIN]:
            cls.setup_admin(defaults)

        cls.setup_extensions(defaults)

        installed_apps = defaults['INSTALLED_APPS']

        app_name = djapp_options[cls.KEY_APP]
        hook = djapp_options.pop(cls._KEY_HOOK, None) or (lambda settings_dict: settings_dict)

        if not app_name:
            project_mode = getattr(getattr(hook, 'func', None), '__name__', '') == 'update_settings_from_module'
            # djangoapp is considered testing a whole project (a set of apps)
            # if hook function is a `partial` for a function with the certain name.

            app_name, (testapp_dir, testapp_name) = cls.deduce_apps(
                dir_current=pytest_config.invocation_dir,
                project_mode=project_mode
            )

            if testapp_name:
                installed_apps.append(testapp_name)

                if (testapp_dir / 'urls.py').exists():
                    # Set customized `urls.py`.
                    defaults['ROOT_URLCONF'] = f'{testapp_name}.urls'

        if app_name and (app_name not in installed_apps):
            installed_apps.append(app_name)

        djapp_options[cls.KEY_APP] = app_name

        defaults = hook(defaults)

        return defaults

    @classmethod
    def get_dict(cls) -> dict:
        """Returns current configuration as a dict."""
        return cls.get()[cls._prefix]
