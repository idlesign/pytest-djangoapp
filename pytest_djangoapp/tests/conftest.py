from pytest_djangoapp import configure_djangoapp_plugin


def hook(settings):
    settings['HOOKED'] = True
    return settings


pytest_plugins = configure_djangoapp_plugin(

    admin_contrib=True,

    extend_INSTALLED_APPS=[
        'django.contrib.sites',
    ],

    extend_MIDDLEWARE=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',  # Bogus doubled check.
    ],

    extend_DATABASES={
        'dummy': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    },

    settings_hook=hook,
    migrate=False,

)
