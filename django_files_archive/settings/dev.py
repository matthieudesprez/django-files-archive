# -*- coding: utf-8 -*-
from .common import *

DEBUG = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ALLOWED_HOSTS += ('localhost', '127.0.0.1')

LOGGING["handlers"]["console"]["class"] = "logging.StreamHandler"

DJANGO_FILES_ARCHIVE_OPTIONS["RUN_MODE"] = "dev"
