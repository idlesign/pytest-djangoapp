import pytest

from django import VERSION


@pytest.fixture()
def check_migrations(command_run):
    """Check if migrations are up to date (migration files exist for current models' state).

    Example::

        def test_this(check_migrations):
            result = check_migrations()

    :param str command_name: Command name to run.

    """
    if VERSION < (2, 0):
        raise Exception('Django 2.0+ required for checking migrations')

    def check_migrations_run_(app=None):

        try:
            args = ['--check', '--dry-run']

            if app:
                args.append(app)

            command_run('makemigrations', args=args)

        except SystemExit:
            return False

        return True

    return check_migrations_run_
