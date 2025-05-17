# pytest-djangoapp

<https://github.com/idlesign/pytest-djangoapp>

[![PyPI - Version](https://img.shields.io/pypi/v/pytest-djangoapp)](https://pypi.python.org/pypi/pytest-djangoapp)
[![License](https://img.shields.io/pypi/l/pytest-djangoapp)](https://pypi.python.org/pypi/pytest-djangoapp)
[![Coverage](https://img.shields.io/coverallsCoverage/github/idlesign/pytest-djangoapp)](https://coveralls.io/r/idlesign/pytest-djangoapp)
[![Docs](https://img.shields.io/readthedocs/pytest-djangoapp)](https://pytest-djangoapp.readthedocs.io/)


## Description

*Nice pytest plugin to help you with Django pluggable application testing.*

This exposes some useful tools for Django applications developers to facilitate tests authoring, including:

* Settings overriding
* Template tags testing
* User creation
* Request object creation
* Management command calls
* Mailing
* Migrations
* Messages
* DB queries audit
* Live server & client UI testing
* etc.

Suitable for testing apps for Django 1.8+.


## How to use

Let's say you have classical tests placing (inside application directory):

```
package_dir
|__ myapp
|  |__ __init__.py
|  |__ tests
|  |  |__ __init__.py
|  |  |__ conftest.py  <- Configure djangoapp here.
|
|__ pyproject.toml
```

Add the following lines into `conftest.py` to configure `djangoapp` and start using it:

```python title="conftest.py"
from pytest_djangoapp import configure_djangoapp_plugin

pytest_plugins = configure_djangoapp_plugin()
```

Fixtures usage examples can be found in the documentation and the source code.


## Testing an entire project

Despite the fact that `djangoapp` is primarily aimed to reusable
Django applications testing one can use it also to test a project (a set of apps).
For that, pass a dotted settings module path into `settings` argument:

```python
pytest_plugins = configure_djangoapp_plugin(
    settings='myproject.settings.settings_testing',
    migrate=False,  # If you do not want to apply migrations.
)
```


## What about pytest-django

`pytest-djangoapp` does not depend on `pytest-django`.

There are design decisions in `pytest-django` that might make it uncomfortable to work with.

1. It uses `setuptools` entrypoints feature for `pytest` plugin discovery. It's not a problem by itself,
   but all kinds of bootstrapping with side effects made by `pytest-django` just on startup,
   make the plugin a poor choice for cases of system-wide (i.e. not venv) installations.

2. Philosophy that next to no unit test should require DB access may be quite annoying.

3. Some fixtures (e.g. `django_assert_num_queries`) usability arouse questions.

Despite that `pytest-django` is nice, of course.

`pytest-djangoapp` fixtures allow the use of Django without marking all relevant tests as needing
a database, as is required by pytest-django which provides the ``django_db`` mark and db fixtures.

If you have `pytest-django` already installed, it can be disabled for projects
using `pytest-djangoapp` by adding the following lines into ``pytest.ini``:

```ini title="pytest.ini"
[pytest]
addopts = -p no:django
```

## Documentation

http://pytest-djangoapp.readthedocs.io/
