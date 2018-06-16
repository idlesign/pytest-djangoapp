# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings as django_settings
from django.core.management import call_command
from django.test.runner import DiscoverRunner

from .fixtures import *
from .toolbox import Configuration

assert fixtures_registered  # Just to prevent IDE from import removal on optimization.

runner = DiscoverRunner(interactive=False, verbosity=1)
setup_databases = runner.setup_databases
teardown_databases = runner.teardown_databases


def pytest_runtest_setup(item):
    # todo optional db initialization
    item.old_config = setup_databases()


def pytest_runtest_teardown(item, nextitem):
    call_command('flush', interactive=False)
    teardown_databases(item.old_config)


def pytest_configure(config):
    import django

    settings_dict = Configuration.get_combined(config)

    django_settings.configure(**settings_dict)
    django.setup()
