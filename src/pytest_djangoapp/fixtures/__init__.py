from .commands import command_run, command_makemigrations
from .db import db_queries
from .live import liveserver, liveclient
from .mail import mail_outbox
from .messages import messages
from .migrations import check_migrations
from .request import request_factory, request_get, request_post, request_client
from .settings import settings
from .templates import template_render_tag, template_context, template_strip_tags
from .users import user_create, user_model, user
from .utils import conf_app_name, run_app

fixtures_registered: bool = True
