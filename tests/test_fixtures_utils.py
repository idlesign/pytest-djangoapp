from unittest.mock import patch


def test_conf_app_name(conf_app_name):

    assert conf_app_name == 'pytest_djangoapp'


def test_run_app(run_app, user_model):

    with patch('django.core.management.commands.runserver.Command.run') as patched:
        run_app(username='a', password='b')
        assert patched.called

    assert user_model.objects.filter(username='a').exists()
