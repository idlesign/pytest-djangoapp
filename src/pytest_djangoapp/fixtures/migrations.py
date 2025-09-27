import pytest
from django import VERSION

from ..exceptions import DjangoappException


@pytest.fixture
def check_migrations(command_makemigrations):
    """Check if migrations are up to date (migration files exist for current models' state).

    ```py
        def test_this(check_migrations):
            result = check_migrations()
    ```

    :param app: Application name to check migrations for.

    """
    def check_migrations_(app: str = ''):
        if VERSION < (2, 0):
            raise DjangoappException('Django 2.0+ required for checking migrations') from None

        try:
            command_makemigrations(app=app, args=['--check', '--dry-run'])

        except SystemExit:
            return False

        return True

    return check_migrations_
