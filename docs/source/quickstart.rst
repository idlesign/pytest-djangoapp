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


Using fixtures
--------------

Use them just as you usually do with `pytest`:

.. code-block:: python

    # test_some.py

    def test_this(settings):

        # We use `settings` fixture to temporarily override
        # project settings.
        settings.update({
            'DEBUG': True,
            'MYVAR': 'someval',
        })

        # Now do some testing, with settings overridden.
