import re
import pytest

from django import VERSION


@pytest.mark.skipif(VERSION < (2, 0), reason='Django 2.0+ required')
def test_check_migrations_missing(check_migrations):
    result = check_migrations('testapp_missing_migrations')
    assert result is False, 'Migrations should be missing in testapp_missing_migrations'


@pytest.mark.skipif(VERSION < (2, 0), reason='Django 2.0+ required')
def test_check_migrations_ok(check_migrations):
    result = check_migrations()
    assert result, (
        "ERROR: Migrations check failed! Models' changes not migrated, "
        "please run './manage.py makemigrations' to solve the issue!"
    )


@pytest.mark.skipif(VERSION >= (2, 0), reason='Testing Django 1.9- required')
def test_old_django(check_migrations):
    with pytest.raises(Exception, match=re.escape('Django 2.0+ required for checking migrations')):
        check_migrations()
