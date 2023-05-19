from unittest.mock import MagicMock


def test_liveserver(liveserver, liveclient):

    with liveserver(host='localhost', port=33445) as server:
        assert server.url == 'http://localhost:33445'


def test_selenium(liveserver, liveclient, monkeypatch):

    monkeypatch.setattr('django.test.selenium.SeleniumTestCaseBase', MagicMock())

    with liveserver() as server:

        with liveclient('selenium', browser='firefox') as client:
            selenium = client.handle

            selenium.get(server.url)
            assert 'MagicMock' in f"{selenium.find_element('tag name', 'h1').text}"
