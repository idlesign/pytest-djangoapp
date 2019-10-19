# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from django.core.management import call_command


@pytest.fixture
def command_run():
    """Allows management command run.

    Example::

        def test_this(command_run, capsys):
            result = command_run('my_command', args=['one'], options={'two': 'three'})
            out, err = capsys.readouterr()


    .. warning:: Django < 1.10 will always return `None`, no matter what command returns.

    :param str|unicode command_name: Command name to run.
    :param list args: Required arguments to pass to a command.
    :param dict options: Optional arguments to pass to a command.

    :returns: Command output.

    """
    def command_run_(command_name, args=None, options=None):
        args = args or []
        options = options or {}
        return call_command(command_name, *args, **options)

    return command_run_
