from pathlib import Path
from threading import local
from typing import Callable

_THREAD_LOCAL = local()
setattr(_THREAD_LOCAL, 'configuration', {})


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
            settings_dict: dict = None,
            *,
            app_name: str = None,
            admin_contrib: bool = False,
            settings_hook: Callable = None,
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

        settings_dict = dict(

            SECRET_KEY='djangoapp',

            ALLOWED_HOSTS=(
                global_settings.ALLOWED_HOSTS +
                # testserver Satisfy Django test client needed in Django < 2.0
                ['testserver', '127.0.0.1', 'localhost']
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

            EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',

            TEMPLATES=[
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'APP_DIRS': True,
                    'OPTIONS': {'context_processors': ['django.contrib.messages.context_processors.messages']}
                },
            ],

        )

        return settings_dict.copy()

    @classmethod
    def check_src_dir(cls, *, dir_parent) -> bool:
        dir_src = dir_parent / 'src'
        return dir_src.exists()

    @classmethod
    def deduce_apps(cls, *, dir_current, project_mode: bool) -> tuple[str, tuple[str, str]]:
        testapp_name = ''
        dir_tests = None
        # We try to support
        #   * classic django tests:
        #     app/
        #     - tests/
        #   * separate tests:
        #     app/
        #     tests/
        # and both the above with `src` layout and without
        # and run from `tests` directory and from `root`.

        src_layout = cls.check_src_dir(dir_parent=dir_current)

        if src_layout:
            # run from project dir
            app_name = 'tests'
        else:
            # maybe run from tests/ dir
            app_name = dir_current.basename

        if app_name == 'tests':
            # support both `src` layout (e.g. to test djangoapp itself)
            # and src-less layouts (with tests inside an app).
            dir_parent = dir_current.parts()[-2]
            src_layout = src_layout or cls.check_src_dir(dir_parent=dir_parent)
            if not src_layout:
                app_name = dir_parent.basename

            dir_tests = dir_current

        try:
            dir_tests = dir_current.listdir('tests')[0]

        except IndexError:
            pass

        if not dir_tests:
            # No `tests` subdir found. Let's try to deduce.
            import py

            app_name = ''
            candidate_latest = ''
            candidates = []

            packages_found = [
                f"{obj}"
                for obj in dir_current.listdir()
                if obj.isdir() and (obj / '__init__.py').exists()
            ]

            for package in packages_found:
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

        if not app_name and not project_mode:
            raise Exception(
                'Unable to deduce application name. '
                'Check application package and `tests` directory exists. '
                f'Current dir: {dir_current}')

        testapp_dir = ''

        if dir_tests:
            # Try to find and an additional test app.
            testapp_dir_name = cls.DIR_TESTAPP
            testapp_dir = dir_tests.listdir(testapp_dir_name)

            if testapp_dir:
                testapp_dir = f'{testapp_dir[0]}'

                prefix = f'{app_name}.'
                if app_name != 'tests':
                    prefix = f'{prefix}tests.'

                testapp_name = f'{prefix}{testapp_dir_name}'

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

                if (Path(testapp_dir) / 'urls.py').exists():
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
