from typing import List, Dict

import pytest

from collections import defaultdict

if False:  # pragma: nocover
    from django.contrib.messages.storage.base import Message  # noqa


class DjangoappMessageStorage:

    def __init__(self):
        self.all: List['Message'] = []
        self.tags: Dict[str, List['Message']] = defaultdict(list)

    def __contains__(self, item):
        for msg in self.all:
            if item in f'{msg}':
                return True

        return False

    def __len__(self):
        return len(self.all)

    def add(self, level, message, extra_tags=''):
        from django.contrib.messages.storage.base import Message

        msg = Message(level, message, extra_tags)
        self.all.append(msg)
        self.tags[msg.level_tag].append(msg)


@pytest.fixture
def messages(monkeypatch) -> DjangoappMessageStorage:
    """Holds messages sent by Django Messages framework.

    Attributes:
      * all -- a list of all messages
      * tags -- messages dictionary indexed by tags

    ```py
    def test_this(messages):
        assert len(messages.all)
        assert len(messages.tags['error'])
        assert 'another error' in messages
    ```

    """
    messages = DjangoappMessageStorage()

    def add(request, level, message, extra_tags='', **kwargs):
        messages.add(level, message, extra_tags)

    monkeypatch.setattr('django.contrib.messages.api.add_message', add)

    return messages
