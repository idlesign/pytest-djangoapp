import pytest

from pytest_djangoapp.configuration import Configuration


def test_configuration(pytestconfig):

    settings = Configuration.get()
    settings[Configuration.KEY_APP] = 'some'

    assert Configuration.get_combined(pytestconfig)

    settings[Configuration.KEY_APP] = ''
    assert Configuration.get_combined(pytestconfig)

    def swap_dir(level):

        old_dir = pytestconfig.invocation_dir

        try:
            pytestconfig.invocation_dir = old_dir.parts()[level]
            assert Configuration.get_combined(pytestconfig)

        finally:
            pytestconfig.invocation_dir = old_dir

    with pytest.raises(Exception):
        # Unable to deduce app name.
        swap_dir(-4)


@pytest.fixture
def check_deduce():
    def check_deduce_(*, cwd, app_name, testapp_dir, testapp_name):
        app_name_, (testapp_dir_, testapp_name_) = Configuration.deduce_apps(dir_current=cwd)
        testapp_dir_ = f'{testapp_dir_ or ""}'
        assert app_name_ == app_name

        if testapp_dir:
            assert testapp_dir_.endswith(testapp_dir), f'"{testapp_dir}" not in "{testapp_dir_}"'
        else:
            assert testapp_dir_ == testapp_dir

        assert testapp_name_ == testapp_name

    return check_deduce_


@pytest.mark.parametrize('layout_flat', [True, False])
@pytest.mark.parametrize('layout_src', [True, False])
@pytest.mark.parametrize('run_in_base_dir', [True, False])
def test_deduce_apps(layout_flat, layout_src, run_in_base_dir, tmpdir, check_deduce):
    """
    Classic django app structure:
        [src]
          - app
            - tests

    Flat django app structure:
        [src]
          - app
          - tests
    """
    dir_base = tmpdir.mkdir('base')

    dir_src = None
    src_marker = ''
    if layout_src:
        dir_src = dir_base.mkdir('src')
        src_marker = 'src/'

    dir_app = (dir_src or dir_base).mkdir('app')
    dir_tests = (dir_base if layout_flat else dir_app).mkdir('tests')

    with pytest.raises(Exception, match='Unable to deduce application name'):
        Configuration.deduce_apps(dir_current=dir_base)

    cwd = dir_base if run_in_base_dir else dir_tests

    # mock an app package -- no testapp
    (dir_app / '__init__.py').write(b'')
    (dir_tests / '__init__.py').write(b'')

    check_deduce(cwd=cwd, app_name='app', testapp_dir='', testapp_name= '')

    # now mock a test app
    dir_testapp = dir_tests.mkdir('testapp')
    (dir_testapp / 'urls.py').write(b'')

    check_deduce(
        cwd=cwd,
        app_name='app',
        testapp_dir=(
            "base/tests/testapp"
            if layout_flat else
            f"base/{src_marker}app/tests/testapp"
        ),
        testapp_name="tests.testapp" if layout_flat else "app.tests.testapp"
    )


def test_settings_hook():
    from django.conf import settings
    assert settings.HOOKED
