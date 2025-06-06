import os
from datetime import timedelta

from random import random

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = (os.getenv("DEBUG") != "false")  # SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = os.getenv("SECRET_KEY") or "wow so secret"
ALLOWED_HOSTS = ["46.229.214.38", "localhost", "127.0.0.1"]
INTERNAL_IPS = ["127.0.0.1"]
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_bleach",
    "boards",
    "parsing",
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    # если есть другие — добавляй сюда
]


ROOT_URLCONF = "infomate.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "boards.context_processors.settings_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "infomate.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB") or "infomate",
        "USER": os.getenv("POSTGRES_USER") or "postgres",
        "PASSWORD": os.getenv("POSTGRES_PASSWORD") or "",
        "HOST": os.getenv("POSTGRES_HOST") or "localhost",
        "PORT": os.getenv("POSTGRES_PORT") or 5432,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_URL = "/static/"
CSS_HASH = str(random())

# Cache

if DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": "/tmp/infomate_cache"
        }
    }

STATIC_PAGE_CACHE_SECONDS = 5 * 60  # 5 min
BOARD_CACHE_SECONDS = 10 * 60  # 10 min

# App settings

APP_NAME = "Infomate"
APP_TITLE = "Агрегатор инфополя"
APP_DESCRIPTION = APP_TITLE
APP_HOST = os.getenv("APP_HOST") or "http://127.0.0.1:8000"

SENTRY_DSN = os.getenv("SENTRY_DSN")

MEDIA_UPLOAD_URL = "https://i.vas3k.ru/upload/"
MEDIA_UPLOAD_CODE = os.getenv("MEDIA_UPLOAD_CODE")

TELEGRAM_CACHE_SECONDS = 10 * 60  # 10 min

BLEACH_STRIP_TAGS = True

OLD_ARTICLES_CLEANUP_AFTER_DAYS = 300
OLD_ARTICLES_CLEANUP_AFTER_AMOUNT = 150

if SENTRY_DSN and not DEBUG:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()]
    )

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
