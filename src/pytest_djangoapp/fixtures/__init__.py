from .admin import admin_client
from .commands import command_makemigrations, command_run
from .db import db_queries
from .live import liveclient, liveserver
from .mail import mail_outbox
from .messages import messages
from .migrations import check_migrations
from .request import request_client, request_factory, request_get, request_post
from .settings import settings
from .templates import template_context, template_render_tag, template_strip_tags
from .users import user, user_create, user_model
from .utils import conf_app_name, registered_urls, run_app

fixtures_registered: bool = True
