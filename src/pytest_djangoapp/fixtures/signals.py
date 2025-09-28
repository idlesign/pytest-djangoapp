from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, ClassVar, Iterable

import pytest
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.signals import Signal, got_request_exception, request_finished, request_started, setting_changed
from django.db.backends.signals import connection_created
from django.db.models.signals import (
    class_prepared,
    m2m_changed,
    post_delete,
    post_init,
    post_migrate,
    post_save,
    pre_delete,
    pre_init,
    pre_migrate,
    pre_save,
)
from django.test.signals import template_rendered

try:
    from django.utils.autoreload import autoreload_started, file_changed

except ImportError:  # fake for django <2.2
    autoreload_started = Signal()
    file_changed = Signal()


@dataclass(slots=True)
class Captured:
    """Captured signal information."""
    name: str
    sender: Any
    kwargs: dict

    def __str__(self):
        return f'[{self.name}] {self.sender} {self.kwargs}'


class DjangoappSignalsStorage:
    """Stores information about signals."""

    builtin_signals: ClassVar[list[Signal]] = [
        request_started, request_finished, got_request_exception, setting_changed,
        user_logged_in, user_logged_out,
        connection_created,
        class_prepared, pre_init, post_init, pre_save, post_save, pre_delete, post_delete, m2m_changed,
        pre_migrate, post_migrate,
        template_rendered,
        autoreload_started, file_changed,
    ]

    def __init__(self):
        self._watched: dict[Signal, str] = {}
        self.captured: list[Captured] = []
        self.captured_by_name: dict[str, list[Captured]] = defaultdict(list)

    def __len__(self):
        return len(self.captured)

    def _receiver(self, sender: Any, signal: Signal, **kwargs):
        # handle old-style with args
        kwargs.pop('args', None)
        if kwargs_ := kwargs.pop('kwargs', None):
            kwargs = kwargs_

        name = self._watched.get(signal, None)
        captured = Captured(
            name=name,
            sender=sender,
            kwargs=kwargs
        )

        self.captured.append(captured)
        self.captured_by_name[name].append(captured)

    def _watch(self, signals: Iterable[Signal] | None = None):
        receiver = self._receiver
        watched = self._watched
        globals_map = {id(obj): name for name, obj in globals().items()}

        for signal in signals or signals or self.builtin_signals:
            signal_obj_id = id(signal)
            known_name = globals_map.get(signal_obj_id, '???')  # ??? -> user supplied
            signal.connect(receiver)
            watched[signal] = known_name

    def _drop(self):
        self._watched.clear()

    def capture(self, signals: Iterable[Signal] | None = None):
        self._watch(signals)
        return self

    def __enter__(self, signals: Iterable[Signal] | None = None) -> DjangoappSignalsStorage:  # noqa: PYI034
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._drop()


@pytest.fixture
def signals():
    """Allows capturing messages sent with Django Signals.

    ```py
    def test_signaling(signals):
        with signals.capture():
            MyModel().save()

        assert len(signals) == 4
        assert signals.captured
        assert signals.captured_by_name
    ```

    """
    return DjangoappSignalsStorage()
