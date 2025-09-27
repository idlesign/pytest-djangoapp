from time import time

import pytest
from django.urls import get_resolver
from django.urls.resolvers import URLResolver

from ..configuration import Configuration


def get_stamp() -> str:
    """Returns current timestamp as a string."""
    return f'{time()}'


@pytest.fixture
def registered_urls() -> dict:
    """Returns mapping from registered urlpatterns to names and args.

    ```py
    def test_me(registered_urls):
        assert 'admin:testapp_article_change object_id' in f'{registered_urls}'
    ```

    """
    patterns = {}

    def clean_url(prefix, postfix) -> str:
        prefix = f'{prefix}'.strip(' ^$')
        postfix = f'{postfix}'.strip(' ^$')
        return f'{prefix}{postfix}'.replace('\\\\', "\\")

    def gather(resolver, *, url_prefix: str, parent_namespace: str, container: dict):
        namespace = resolver.namespace or parent_namespace
        url_prefix = clean_url(url_prefix, resolver.pattern)

        for item in resolver.url_patterns:
            subcontainer = container.setdefault(namespace, {}) if namespace != parent_namespace else container

            if isinstance(item, URLResolver):
                gather(item, url_prefix=url_prefix, parent_namespace=namespace, container=subcontainer)
            else:
                pattern = item.pattern
                args = ' '.join(pattern.converters)
                subcontainer[clean_url(url_prefix, pattern)] = (
                    f'{namespace}:{pattern.name or "???"} {args}'.strip(': ')
                )

    gather(get_resolver(), url_prefix='', parent_namespace='', container=patterns)

    return patterns


@pytest.fixture(scope='session')#
def conf_app_name() -> str:
    """Returns your application name (deduced or provided)."""
    return Configuration.get_dict()[Configuration.KEY_APP]


@pytest.fixture
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

