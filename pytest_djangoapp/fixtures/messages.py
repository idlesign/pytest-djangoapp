import pytest

from collections import defaultdict

from .utils import text_type


class DjangoappMessageStorage(object):

    def __init__(self):
        self.all = []
        self.tags = defaultdict(list)

    def __contains__(self, item):
        for msg in self.all:
            if item in text_type(msg):
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
def messages(monkeypatch):
    """Holds messages sent by Django Messages framework.

    Attributes:
        * all -- a list of all messages
        * tags -- messages dictionary indexed by tags

    Example::

        def test_this(messages):
            assert len(messages.all)
            assert len(messages.tags['error'])
            assert 'another error' in messages

    :rtype: DjangoappMessageStorage

    """
    messages = DjangoappMessageStorage()

    def add(request, level, message, extra_tags='', **kwargs):
        messages.add(level, message, extra_tags)

    monkeypatch.setattr('django.contrib.messages.api.add_message', add)

    return messages
