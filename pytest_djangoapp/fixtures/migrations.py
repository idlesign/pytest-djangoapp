import pytest

from django import VERSION


@pytest.fixture()
def check_migrations(command_run):
    """Check if migrations are up to date (migration files exist for current models' state).

    Example::

        def test_this(check_migrations):
            result = check_migrations()

    :param app: Application name to check migrations for.

    """
    def check_migrations_run_(app: str = None):
        if VERSION < (2, 0):
            raise Exception('Django 2.0+ required for checking migrations')

        try:
            args = ['--check', '--dry-run']

            if app:
                args.append(app)

            command_run('makemigrations', args=args)

        except SystemExit:
            return False

        return True

    return check_migrations_run_
