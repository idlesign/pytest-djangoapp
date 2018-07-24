from django.core.mail import send_mail


def test_mail_outbox(mail_outbox):

    send_mail(
        'Subject here', 'Here is the message.',
        'from@example.com', ['to@example.com'],
        fail_silently=False,
    )

    assert len(mail_outbox) == 1
    assert mail_outbox[0].subject == 'Subject here'
