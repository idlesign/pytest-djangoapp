import io
import os
import re
import sys

from setuptools import setup, find_packages


PY2 = sys.version_info[0] == 2
PATH_BASE = os.path.dirname(__file__)
PYTEST_RUNNER = ['pytest-runner'] if 'test' in sys.argv else []


def read_file(fpath):
    """Reads a file within package directories."""
    with io.open(os.path.join(PATH_BASE, fpath)) as f:
        return f.read()


def get_version():
    """Returns version number, without module import (which can lead to ImportError
    if some dependencies are unavailable before install."""
    contents = read_file(os.path.join('pytest_djangoapp', '__init__.py'))
    version = re.search('VERSION = \(([^)]+)\)', contents)
    version = version.group(1).replace(', ', '.').strip()
    return version


install_requires = [
    'pytest',
]


if PY2:
    install_requires.append('mock')  # unittest.mock only since Python 3.3


setup(
    name='pytest-djangoapp',
    version=get_version(),
    url='https://github.com/idlesign/pytest-djangoapp',

    description='Nice pytest plugin to help you with Django pluggable application testing.',
    long_description=read_file('README.rst'),
    license='BSD 3-Clause License',

    author='Igor `idle sign` Starikov',
    author_email='idlesign@yandex.ru',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=install_requires,
    setup_requires=[] + PYTEST_RUNNER,
    tests_require=['pytest'],

    test_suite='tests',

    classifiers=[
        # As in https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: BSD License'
    ],
)


