from functools import partial
from typing import Union, Callable

from .configuration import Configuration


def configure_djangoapp_plugin(
    settings: Union[str, dict] = None,
    *,
    app_name: str = None,
    admin_contrib: bool = False,
    settings_hook: Callable = None,
    migrate: bool = True,
    **kwargs
) -> str:
    """Configures djangoapp pytest plugin.

    :param settings: Django project settings to override defaults.
        To get settings from a module (for testing an entire project, not just one app)
        use a string with the module name.

    :param app_name: Name of your application you write tests for.
        If not set ``djangoapp`` will try to guess (``tests`` dir needs to be inside application directory).

    :param admin_contrib: Setup Django to test Admin contrib related parts.

    :param settings_hook: Allows setting a function to get resulting settings.

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

    """
    try:
        import django

    except ImportError:  # pragma: nocover
        raise Exception('Django is not available in test environment. Please install it.')

    if isinstance(settings, str):
        # Considering a whole project testing mode.
        settings_hook = partial(update_settings_from_module, module=settings)
        settings = {}

    Configuration.set(
        settings_dict=settings,
        app_name=app_name,
        admin_contrib=admin_contrib,
        settings_hook=settings_hook,
        migrate=migrate,
        **kwargs
    )

    return 'pytest_djangoapp.plugin'


def update_settings_from_module(settings: dict, *, module: str) -> dict:
    """Updates a given settings dict from a module denoted by a dotted path.

    :param settings:
    :param module:

    """
    from importlib import import_module

    settings_module = import_module(module)

    settings_dict = {
        key: value
        for key, value in settings_module.__dict__.items()
        if key.upper() == key and not key.startswith('_')
    }
    settings.update(settings_dict)

    return settings
