import os
from pathlib import Path

import environ
from dotenv import find_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()

if DEBUG := env.bool("DEBUG", default=True):
    environ.Env.read_env(find_dotenv(".env"))

DEFAULT = '123:SOMEDEFAULTKEY:TEST'

SECRET_KEY = env.str('SECRET_KEY', default=DEFAULT)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["*"])

AUTH_USER_MODEL = "admin_user.AdminUser"

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_object_actions'
]

LOCAL_APPS = ['bot', 'admin_user']

EXTERNAL_APPS = []

INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + EXTERNAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": env.str("POSTGRES_ENGINE", default='django.db.backends.postgresql'),
        "NAME": env.str("POSTGRES_NAME", default='postgres'),
        "USER": env.str("POSTGRES_USER", default='postgres'),
        "PASSWORD": env.str("POSTGRES_PASSWORD", default='postgres'),
        "HOST": env.str("POSTGRES_HOST", default='localhost'),
        "PORT": env.str("POSTGRES_PORT", default='5432'),
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

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TELEGRAM_TOKEN = env.str('TELEGRAM_TOKEN', default=DEFAULT)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WEBHOOK_ENABLED = env.bool('WEBHOOK_ENABLED', default=False)
WEB_SERVER_HOST = env.str('WEB_SERVER_HOST', default='0.0.0.0')
WEB_SERVER_PORT = env.str('WEB_SERVER_PORT', default=8443)
WEBHOOK_PATH = env.str('WEBHOOK_PATH', default='/webhook')
WEBHOOK_URL = env.str('WEBHOOK_URL', default='localhost')

REDIS = env.bool('REDIS', default=False)
REDIS_HOST = env.str('REDIS_HOST', default='127.0.0.1')
REDIS_PORT = env.str('REDIS_PORT', default=6379)

BUNKER_PLACE_DIVIDER = 2
HEALTH_CHANCE = 30
PHOBIA_CHANCE = 10
ORIENTATION_CHANCE = 50
YOUNG_AGE_CHANCE = 50

MIN_AGE_VALUE = 18
AVERAGE_AGE_VALUE = 40
MAX_AGE_VALUE = 100
