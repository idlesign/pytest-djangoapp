from django.dispatch.dispatcher import Signal

from tests.testapp.models import Article

mysignal = Signal()


def test_signals_default(signals):

    with signals.capture():
        Article().save()
        Article().save()

    assert len(signals) == 8
    assert len(signals.captured_by_name['pre_save']) == 2
    assert signals.captured_by_name['pre_init'][0].kwargs == {}


def test_signals_user(signals):

    with signals.capture([mysignal]):
        mysignal.send('me', a=1, b=2)

    assert len(signals) == 1
    assert f'{signals.captured[0]}' == "[???] me {'a': 1, 'b': 2}"
