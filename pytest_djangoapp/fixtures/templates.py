try:
    from unittest import mock
except ImportError:
    import mock


import pytest

from django import VERSION
from django.template.base import Template
from django.template.context import Context, RenderContext
from six import string_types

if False:  # pragma: nocover
    from django.contrib.auth.base_user import AbstractBaseUser
    from django.http import HttpRequest


@pytest.fixture
def mock_template_context(request_get, user_create):
    """Creates mock Template context.

    To be used with `render_template_tag` fixture.

    Example::

        def test_this(mock_template_context):
            context = mock_template_context({'somevar': 'someval'})

    """
    def mock_template_context_(context_dict=None, request=None, current_app='', user='anonymous'):
        """
        :param dict context_dict:
        :param str|unicode|HttpRequest request:
        :param str|unicode current_app:
        :param AbstractBaseUser user: Defaults to anonymous user will be used.

        :rtype: Context
        """
        context_dict = context_dict or {}

        if user == 'anonymous':
            user = user_create(anonymous=True)

        if not request or isinstance(request, string_types):
            request = request_get(request, user=user)

        context_updater = {
            'request': request,
        }

        if user:
            context_updater['user'] = user

        context_dict.update(context_updater)

        context = Context(context_dict)
        contribute_to_context(context, current_app)

        return context

    return mock_template_context_


@pytest.fixture
def render_template_tag():
    """Renders a template tag from a given library by its name.

    Example::

        def test_this(render_template_tag):
            rendered = render_template_tag('library_name', 'mytag arg1 arg2')


    """
    def render_template_tag_(tag_library, tag_str, context=None):
        """
        :param str|unicode tag_library:
        :param str|unicode tag_str:
        :param Context context:

        :rtype: str|unicode
        """
        context = context or {}

        if not isinstance(context, Context):
            context = Context(context)

        contribute_to_context(context)
        string = '{%% load %s %%}{%% %s %%}' % (tag_library, tag_str)
        template = Template(string)

        if VERSION >= (1, 11):
            # Prevent "TypeError: 'NoneType' object is not iterable" in  get_exception_info
            template.nodelist[1].token.position = (0, 0)

        return template.render(context)

    return render_template_tag_


def contribute_to_context(context, current_app=''):
    template = mock.MagicMock()
    template.engine.string_if_invalid = ''

    context.template = template

    if VERSION >= (1, 11):
        context.render_context = RenderContext()

    if VERSION >= (1, 10):
        match = mock.MagicMock()
        match.app_name = current_app
        context.resolver_match = match

    else:
        context._current_app = current_app
