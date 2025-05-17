from django.conf import settings as django_settings
from django.core.management import call_command
from django.test.runner import DiscoverRunner

from .fixtures import *  # noqa
from .toolbox import Configuration

runner = DiscoverRunner(interactive=False, verbosity=0)
setup_databases = runner.setup_databases
teardown_databases = runner.teardown_databases


def pytest_runtest_setup(item):
    # todo optional db initialization
    item.old_config = setup_databases()


def pytest_runtest_teardown(item, nextitem):
    unset = {}

    old_config = getattr(item, 'old_config', unset)

    if old_config is unset:
        # _teardown will suddenly work even if no _setup has occurred
        # e.g. in case of mark.skipif
        return

    call_command('flush', interactive=False, reset_sequences=False)
    teardown_databases(old_config)


def pytest_configure(config):
    import django

    settings_dict = Configuration.get_combined(config)

    django_settings.configure(**settings_dict)
    django.setup()
    runner.verbosity = config.option.verbose
