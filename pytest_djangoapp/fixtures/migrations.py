import pytest

from django import VERSION
from django.core.management import call_command


@pytest.fixture()
def check_migrations():
    """Check if migrations are up to date.

    Example::

        def test_this(check_migrations):
            result = check_migrations()

    """
    def check_migrations_run_(app=None):
        if VERSION < (2, 0):
            raise Exception('Django 2.0+ required for checking migrations')

        try:
            if app:
                call_command('makemigrations', '--check', '--dry-run', app)
            else:
                call_command('makemigrations', '--check', '--dry-run')
        except SystemExit:
            return False
        return True

    return check_migrations_run_
