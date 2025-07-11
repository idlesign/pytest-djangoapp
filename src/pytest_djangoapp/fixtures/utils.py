from time import time

import pytest
from django.utils import translation

from ..configuration import Configuration


def get_stamp() -> str:
    """Returns current timestamp as a string."""
    return f'{time()}'


@pytest.fixture(scope='session')
def conf_app_name() -> str:
    """Returns your application name (deduced or provided)."""
    return Configuration.get_dict()[Configuration.KEY_APP]


@pytest.fixture()
def run_app(command_run, user_create, capsys, settings):
    """Issues runserver command using current configuration
    (dynamic or defined by user through `configure_djangoapp_plugin()`).

    Useful for manual verification and debug, to have look and feel
    of an enduser project with your app.

    Run the test using the fixture as usual. It'll start Django development server.
    Stop server with Ctrl+C.

    Admin user is automatically created: username=admin password=admin

    ```py
    def test_me(run_app):
        ...
        run_app()
    ```

    """
    def run_app_(*, username: str = 'admin', password: str = 'admin', **kwargs):
        options = {
            'use_reloader': False,
        }

        settings.DEBUG = True
        settings.WSGI_APPLICATION = None  # override possibly provided by user in configure_djangoapp_plugin()

        user_create(superuser=True, attributes={
            'username': username,
            'password': password,
        })

        with capsys.disabled():
            command_run('runserver', options=options)

    return run_app_

