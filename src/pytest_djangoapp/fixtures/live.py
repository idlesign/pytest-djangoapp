from typing import Type, TypeVar, Dict

import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

TypeLiveClient = TypeVar('TypeLiveClient', bound='LiveClient')


@pytest.fixture()
def liveserver() -> Type['LiveServer']:
    """Runs a live server. Available as a context manager.

    .. warning:: For Django >= 4.0

    ```py
    def test_live(liveserver):

        with liveserver() as server:
            print(f'Live server is available at: {server.url}')
    ```
    """
    return LiveServer


@pytest.fixture()
def liveclient():
    """Runs a live client. Available as a context manager.

    ```py
    def test_live(liveserver, liveclient):

        with liveserver() as server:

            # Let's run Firefox using Selenium.
            with liveclient('selenium', browser='firefox') as client:
                selenium = client.handle  # Selenium driver is available in .handle

                # Let's open server's root URL and check heading 1 on that page
                selenium.get(server.url)
                assert selenium.find_element('tag name', 'h1').text == 'Not Found'
    ```

    """
    def get_client(typename: str, *, browser: str) -> TypeLiveClient:
        return LiveClient.spawn(alias=typename, browser=browser)

    return get_client


class LiveServer:

    _cls = StaticLiveServerTestCase

    def __init__(self, *, host: str = None, port: int = None):

        cls = self._cls

        if host:
            cls.host = host

        if port is not None:
            cls.port = port

    @property
    def url(self) -> str:
        """URL to access this live server."""
        return self._cls.live_server_url

    def __enter__(self):
        self._cls._start_server_thread()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cls._terminate_thread()


class LiveClient:
    """Base class for live clients."""

    alias: str = ''

    _registry: Dict[str, TypeLiveClient] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()

        alias = cls.alias

        if alias:
            cls._registry[alias] = cls

    def __init__(self, *, browser: str):
        self._browser = browser
        self.handle = None

    def __enter__(self) -> TypeLiveClient:
        self.handle = self._handle_init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._handle_destroy()

    @classmethod
    def spawn(cls, alias: str, **kwargs) -> TypeLiveClient:
        client_cls = LiveClient._registry[alias]
        return client_cls(**kwargs)

    def _handle_init(self):  # pragma: nocover
        raise NotImplementedError

    def _handle_destroy(self):
        pass


class SeleniumLiveClient(LiveClient):
    """This live client wraps Selenium.

    https://selenium-python.readthedocs.io/

    """
    alias: str = 'selenium'

    def _handle_init(self):
        from django.test.selenium import SeleniumTestCaseBase

        cls = SeleniumTestCaseBase
        browser = self._browser
        driver_cls = cls.import_webdriver(browser)

        return driver_cls(options=cls.import_options(browser)())

    def _handle_destroy(self):

        handle = self.handle

        if handle:
            handle.quit()

        super()._handle_destroy()
