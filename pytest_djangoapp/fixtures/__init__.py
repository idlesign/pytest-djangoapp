# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from .commands import command_run
from .db import db_queries
from .mail import mail_outbox
from .messages import messages
from .request import request_factory, request_get, request_post, request_client
from .settings import settings
from .templates import template_render_tag, template_context, template_strip_tags
from .users import user_create, user_model, user

fixtures_registered = True
