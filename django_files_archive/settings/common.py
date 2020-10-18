# -*- coding: utf-8 -*-
import socket
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DEBUG = False

SECRET_KEY = '___'

ALLOWED_HOSTS = ()

MAIN_APP = 'django_files_archive'
INSTALLED_APPS = (
    'django.contrib.staticfiles',
    MAIN_APP,
)

ROOT_URLCONF = 'django_files_archive.urls'

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(BASE_DIR, 'templates'),),
        'APP_DIRS': True
    },
]

DJANGO_FILES_ARCHIVE_OPTIONS = {
    "RUN_MODE": "unknown",
    "INSTANCE_ID": socket.gethostname(),
    "WORKER_PID": os.getpid(),
    "CACHE_ENABLED": True,
    "DOWNLOAD_ENABLED": True,
    "DOWNLOAD_TIMEOUT": 40,
    "MONITORING_ENABLED": True,
}

DATABASES = {}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'formatters': {
        'basic': {
            'format': '%(levelname)s - %(name)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
            'formatter': 'basic'
        },
    },
    'loggers': {
        'botocore': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'boto3': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
