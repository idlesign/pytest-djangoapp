# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import re

try:
    from unittest import mock
except ImportError:
    import mock

import pytest

from django import VERSION
from django.template.base import Template
from django.template.context import Context, RenderContext

from .utils import string_types


if False:  # pragma: nocover
    from django.contrib.auth.base_user import AbstractBaseUser
    from django.http import HttpRequest


RE_TAG_VALUES = re.compile('>([^<]+)<')


@pytest.fixture
def template_strip_tags():
    """Allows HTML tags strip from string.

    To be used with `template_render_tag` fixture to easy result assertions.

    Example::

        def test_this(template_strip_tags):
            stripped = template_strip_tags('<b>some</b>')

    :param str|unicode html: HTML to strin tags from
    :param str|unicode joiner: String to join tags contents. Default: |

    """
    def template_strip_tags_(html, joiner='|'):
        """
        :rtype: str|unicode
        """
        result = []
        for match in RE_TAG_VALUES.findall(html):
            match = match.strip()
            if match:
                result.append(match)

        return joiner.join(result)

    return template_strip_tags_


@pytest.fixture
def template_context(request_get, user_create):
    """Creates template context object.

    To be used with `template_render_tag` fixture.

    Example::

        def test_this(template_context):
            context = template_context({'somevar': 'someval'})


    :param dict context_dict: Template context. If not set empty context is used.

    :param str|unicode|HttpRequest request: Expects HttpRequest or string.
        String is used as a path for GET-request.

    :param str|unicode current_app:

    :param AbstractBaseUser|str|unicode user: User to associate request with.
        Defaults to anonymous user.


    """
    def template_context_(context_dict=None, request=None, current_app='', user='anonymous'):
        """
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

    return template_context_


@pytest.fixture
def template_render_tag():
    """Renders a template tag from a given library by its name.

    Example::

        def test_this(template_render_tag):
            rendered = template_render_tag('library_name', 'mytag arg1 arg2')

    :param str|unicode library: Template tags library name to load tag from.

    :param str|unicode tag_str: Tag string itself. As used in templates, but without {% %}.

    :param Context context: Template context object. If not set,
        empty context object is used.

    """
    def template_render_tag_(library, tag_str, context=None):
        """
        :rtype: str|unicode
        """
        context = context or {}

        if not isinstance(context, Context):
            context = Context(context)

        string = '{%% load %s %%}{%% %s %%}' % (library, tag_str)

        template = Template(string)
        contribute_to_context(context, template=template)

        if VERSION >= (1, 11):
            # Prevent "TypeError: 'NoneType' object is not iterable" in  get_exception_info
            template.nodelist[1].token.position = (0, 0)

        return template.render(context)

    return template_render_tag_


def contribute_to_context(context, current_app='', template=None):
    template = template or mock.MagicMock()

    if VERSION >= (1, 8):
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
