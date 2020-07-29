# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from .commands import command_run
from .db import db_queries
from .mail import mail_outbox
from .messages import messages
from .request import request_factory, request_get, request_post, request_client
from .settings import app_name, djapp_options, settings
from .templates import template_render_tag, template_context, template_strip_tags
from .urls import (
    fake_global_urlconf_module,
    fake_global_urlpatterns,
    urlpatterns,
    inject_app_urls,
    inject_testapp_urls,
)
from .users import user_create, user_model, user

fixtures_registered = True
