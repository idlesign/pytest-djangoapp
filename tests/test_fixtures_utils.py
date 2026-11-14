from unittest.mock import patch


def test_conf_app_name(conf_app_name):

    assert conf_app_name == 'pytest_djangoapp'


def test_registered_urls(registered_urls):
    assert 'admin:testapp_article_change object_id' in f'{registered_urls}'


def test_run_app(run_app, user_model):

    with patch('django.core.management.commands.runserver.Command.run') as patched:
        run_app(username='a', password='b')
        assert patched.called

    assert user_model.objects.filter(username='a').exists()


def test_reload_modules(tmp_path, monkeypatch, reload_modules):

    pkg = tmp_path / "mypkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    (pkg / "settings.py").write_text("OPTION = 1\n")
    (pkg / "mymod.py").write_text("from .settings import OPTION\n")
    monkeypatch.syspath_prepend(str(tmp_path))

    import mypkg.mymod

    assert mypkg.mymod.OPTION == 1

    settings_file = pkg / "settings.py"
    settings_file.write_text("OPTION = 2\n")

    # Bytecode caches validate by mtime with a one-second resolution.
    import os
    import time
    future = time.time() + 2
    os.utime(settings_file, (future, future))

    reload_modules("mypkg.settings", "mypkg.mymod")

    assert mypkg.mymod.OPTION == 2
