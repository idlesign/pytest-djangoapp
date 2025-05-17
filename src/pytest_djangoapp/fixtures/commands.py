from typing import Iterable, Optional

import pytest

from django.core.management import call_command


@pytest.fixture
def command_run():
    """Allows management command run.

    ```py
    def test_this(command_run, capsys):
        result = command_run('my_command', args=['one'], options={'two': 'three'})
        out, err = capsys.readouterr()
    ```

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


@pytest.fixture
def command_makemigrations(conf_app_name):
    """Allows to run makemigrations command.

    .. note:: This command can be useful to generate
        migrations for your application (without a project creation).

    ```py
    def test_makemigrations(command_makemigrations):
        command_makemigrations()
    ```

    :param app: Application name to run 'makemigrations' for.
        * By default, a name from 'conf_app_name' fixture is used.
        * If empty string, command is run for any application.

    :param args: Additional arguments to pass to the command.

    """
    def command_migration_(*, app: str = None, args: Iterable[str] = None) -> Optional[str]:
        args = args or []

        if app is None:
            app = conf_app_name

        if app:
            args.append(app)

        return call_command('makemigrations', *args)

    return command_migration_
