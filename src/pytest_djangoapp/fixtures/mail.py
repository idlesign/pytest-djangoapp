from typing import List

import pytest

from django.core import mail


mail.outbox = []


@pytest.fixture()
def mail_outbox() -> List[mail.EmailMessage]:
    """Returns mail outbox: list of sent message objects.

    ```py
    def test_this(mail_outbox):
        first_subject = mail_outbox[0].subject
    ```

    """
    yield mail.outbox

    mail.outbox = []
