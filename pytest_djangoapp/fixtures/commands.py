from typing import Iterable, Optional

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

    :param command_name: Command name to run.
    :param args: Required arguments to pass to a command.
    :param options: Optional arguments to pass to a command.

    :returns: Command output.

    """
    def command_run_(command_name: str, args: Iterable[str] = None, options: dict = None) -> Optional[str]:
        args = args or []
        options = options or {}
        return call_command(command_name, *args, **options)

    return command_run_
