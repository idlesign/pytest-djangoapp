Quickstart
==========


Application structuring
-----------------------

Let's say you have classical tests placing (inside application directory)::

    package_dir
    |__ myapp
    |  |__ __init__.py
    |  |__ tests
    |  |  |__ __init__.py
    |  |  |__ conftest.py  <- Configure djangoapp here.
    |
    |__ setup.py



Configuring djangoapp
---------------------

Add the following lines into `conftest.py` to configure `djangoapp` and start using it:


.. code-block:: python

    # conftest.py
    from pytest_djangoapp import configure_djangoapp_plugin

    pytest_plugins = configure_djangoapp_plugin()


You can override default settings:

.. code-block:: python

    pytest_plugins = configure_djangoapp_plugin({
        'DEBUG': False,
        'SOMETHING': 'else,
    })


Sometimes you may want to extend default settings, such as `INSTALLED_APPS` or `DATABASES`.
To do this you can pass `extend_`-prefixed arguments:

.. code-block:: python

    pytest_plugins = configure_djangoapp_plugin(
        extend_INSTALLED_APPS=[
            'django.contrib.sites',
        ],
        extend_MIDDLEWARE=[
            'django.contrib.sessions.middleware.SessionMiddleware',
        ],
        extend_DATABASES={
            'dummy': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
    )


If you test an application providing some integration with Django Admin contrib,
there is a convenient `admin_contrib` argument you can pass to activate this contrib:

.. code-block:: python

    pytest_plugins = configure_djangoapp_plugin(admin_contrib=True)


By default all DB migrations are applied on test runs. Since that can be unnecessary and take a long time,
there is a `migrate` argument that you can always set to ``False``:

.. code-block:: python

    pytest_plugins = configure_djangoapp_plugin(migrate=False)


You can further change or altogether replace generated settings using `settings_hook` argument:

.. code-block:: python

    def hook(settings):
        # Do something with settings.
        return settings

    pytest_plugins = configure_djangoapp_plugin(
        settings_hook=hook,
    )



Testing an entire project
-------------------------

.. note:: Requires Python 3.

Despite the fact that `djangoapp` is primarily aimed to reusable
Django applications testing one can use it also to test a project (a set of apps).
For that, pass a dotted settings module path into `settings` argument:


.. code-block:: python

    pytest_plugins = configure_djangoapp_plugin(
        settings='myproject.settings.settings_testing',
    )


Using fixtures
--------------

Use them just as you usually do with `pytest`:

.. code-block:: python

    # test_some.py

    def test_this(settings, request_client):

        # We use `settings` fixture to temporarily override
        # project settings.
        with settings(DEBUG=True, MYVAR='someval'):
            # Now do some testing, with settings overridden.
            ...

        # And we use `request_client` fixture
        # to test our [AJAX] view.
        client = request_client(ajax=True)

        # We pass a tuple with a view name with arguments to not to bother with URL.
        response = client.get(('someview', {'somearg': 'one', 'otherarg': 33}))

        ...

        # See fixtures documentation for more fixtures.


Additional app for testing
--------------------------

Sometimes your app may provide tooling for other apps (say it automatically imports modules from them,
or provides some urlpatterns). If so, you may want to simulate that other application in your tests.

You can easily do that by adding ``testapp`` package under your test directory (this will be automatically
added to ``INSTALLED_APPS`` and treated by Django just as any application package)::


    package_dir
    |__ myapp
    |  |__ __init__.py
    |  |__ tests
    |  |  |__ __init__.py
    |  |  |__ testapp  <- Thirdparty app simulation package.
    |  |  |  |__ __init__.py
    |  |  |  |__ admin.py  <- This module uses primitives provided by your app.
    |  |  |  |__ models.py  <- This module uses base models provided by your app.
    |  |  |  |__ urls.py  <- And this module uses urlpatterns provided by your app.
    |  |  |__ conftest.py
    |
    |__ setup.py

