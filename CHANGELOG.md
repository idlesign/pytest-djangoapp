# pytest-djangoapp changelog


### v1.4.0 [2025-07-12]
* ++ Add 'run_app' fixture.

### v1.3.0 [2025-06-06]
* !! Dropped QA for Python 3.7.
* ++ Add 'src' package layout.

### v1.2.0 [2023-05-19]

* ++ Add 'liveserver' and 'liveclient' fixtures (closes #24).


### v1.1.0 [2023-03-18]

* ++ Added 'command_makemigrations' fixture.
* ++ Added 'conf_app_name' fixture (see #17).
* ++ Fixture 'template_context' now accepts a username.


### v1.0.0 [2022-11-09]

* ! Dropped support for Django 1.7.
* ! Dropped support for Py2. Py3.6+ specific syntax is introduced. Code update may be required.
* ++ Introduced new 'check_migrations' fixture.


### v0.15.2 [2021-08-04]

* ! Dropped QA for Python 2.7 and 3.5.
* ! This version is the last featuring Python 2 and 3.5 support.
* ** Ignore temporary attributes from project settings module (see #21).


### v0.15.1 [2021-04-10]

* ** Made Django 3.2 compatible.


### v0.15.0 [2020-09-21]

* ++ Fixture 'request_client' now accepts 'json' argument to encode post data.


### v0.14.0 [2020-01-25]

* ++ Added support for testing entire Django projects (requires Py 3).
* ** Added QA for Py3.8 and Django 3.0.


### v0.13.0 [2019-11-23]

* ++ 'request_client' HTTP methods now can accept a tuple of view name with params instead of actual URL path.


### v0.12.0 [2019-10-19]

* ++ Added 'db_queries' fixture.
* ++ Fixture 'request_client' now accepts 'raise_exceptions' argument to tech technical error views.
* ** Added QA for py3.7 and Django 2.2.
* ** Dropped QA for py3.4.
* ** Fix PyCharm hints for some fixtures.


### v0.11.0

* ++ 'configure_djangoapp_plugin()' now accepts 'migrate' argument.
* ** Silenced DB creation/teardown messages.


### v0.10.1
-
* ** Fixed 'pytest_runtest_teardown' failure in case of makr.skipif or similar.


### v0.10.0
-
* ++ 'configure_djangoapp_plugin()' now accepts 'settings_hook' argument.
* ++ Added 'messages' fixture.


### v0.9.0

* ++ 'configure_djangoapp_plugin()' now accepts 'admin_contrib' argument.
* ++ 'request_client' fixture now accepts 'user' argument for easy auth.
* ++ Added 'compat' module with 'get_urlpatterns()' helper.
* ++ User password is now accessible via 'password_plain' attribute of user objects created with fixtures.


### v0.8.0

* ++ Added 'mail_outbox' fixture.


### v0.7.1

* ** Fixed 'extend_' prefixed args handling in old Django versions.


### v0.7.0

* ++ 'configure_djangoapp_plugin()' now accepts 'extend_' prefixed args.


### v0.6.0

* ++ 'request_client' and 'request_factory' and co fixtures now accept 'ajax' argument.


### v0.5.0

* ++ 'settings' fixture now can be used as a context manager.


### v0.4.2

* ** Improved templatetags compatibility for 1.8, 1.9.


### v0.4.1

* ** Added mock package adaptive autoinstall.


### v0.4.0

* ++ Introduced 'command_run' fixture.
* ** Removed six dependency.


### v0.3.2

* ** Added STATIC_URL default.


### v0.3.1

* ** Fixed test client work on Django < 2.0.


### v0.3.0

* ++ Introduced 'request_client' fixture.
* ++ Introduced 'request_post' fixture.
* ++ Introduced 'user' shortcut fixture.


### v0.2.0

* ++ Improved test discovery.
* ++ Introduced 'template_strip_tags' fixture.


### v0.1.0

* ++ Basic functionality.