# -*- encoding: utf-8 -*-
from __future__ import unicode_literals


def test_messages(messages):

    assert not messages.all

    from django.contrib import messages as djmessages

    djmessages.error(None, 'this is error')
    djmessages.error(None, 'ещё ошибка')
    djmessages.info(None, 'some info')

    assert len(messages) == 3
    assert len(messages.tags['error']) == 2
    assert len(messages.tags['info']) == 1

    assert 'ещё ошибка' in messages
    assert 'other' not in messages
