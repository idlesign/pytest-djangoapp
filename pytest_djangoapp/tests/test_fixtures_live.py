from unittest.mock import MagicMock

import pytest
from django import VERSION


@pytest.mark.skipif(VERSION < (4, 0), reason='For Django 4.0+')
def test_liveserver(liveserver, liveclient):

    with liveserver(host='localhost', port=33445) as server:
        assert server.url == 'http://localhost:33445'


@pytest.mark.skipif(VERSION < (4, 0), reason='For Django 4.0+')
def test_selenium(liveserver, liveclient, monkeypatch):

    monkeypatch.setattr('django.test.selenium.SeleniumTestCaseBase', MagicMock())

    with liveserver() as server:

        with liveclient('selenium', browser='firefox') as client:
            selenium = client.handle

            selenium.get(server.url)
            assert 'MagicMock' in f"{selenium.find_element('tag name', 'h1').text}"
