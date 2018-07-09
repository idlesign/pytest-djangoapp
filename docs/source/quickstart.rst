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
        response = client.get('/that')
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
    |  |  |  |__ models.py  <- This module uses base models provided by your app.
    |  |  |  |__ urls.py  <- And this module uses urlpatterns provided by your app.
    |  |  |__ conftest.py
    |
    |__ setup.py

