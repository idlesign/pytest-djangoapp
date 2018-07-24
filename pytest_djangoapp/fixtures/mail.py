# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from django.core import mail


mail.outbox = []


@pytest.fixture()
def mail_outbox():
    """Returns mail outbox: list of sent message objects.

    Example::

        def test_this(mail_outbox):
            first_subject = mail_outbox[0].subject

    :rtype: list[mail.EmailMessage]

    """
    yield mail.outbox

    mail.outbox = []
