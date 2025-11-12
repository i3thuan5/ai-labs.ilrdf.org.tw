import os
from .settings import *  # noqa

# Core

DEBUG = False
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
VIRTUAL_HOST = os.getenv('VIRTUAL_HOST').split(',')
ALLOWED_HOSTS = VIRTUAL_HOST

# Static Files

STATIC_ROOT = '/staticfiles/'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        "USER": os.getenv('POSTGRES_USER'),
        "PASSWORD": os.getenv('POSTGRES_PASSWORD'),
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# Security

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_HTTPONLY = True
LANGUAGE_COOKIE_SECURE = True
LANGUAGE_COOKIE_SAMESITE = "Strict"
LANGUAGE_COOKIE_HTTPONLY = True

# Wagtail

WAGTAILADMIN_BASE_URL = VIRTUAL_HOST[0]


if os.getenv('TOX_CHECKDEPLOY', default=False):
    # Django Deploy檢查有建議ài設定以下項目，
    # 因為下底設定實際上攏tī nginx-proxy做，
    # Django毋免做。
    # Django Deploy檢查ê時暫時先開--開。
    SECURE_HSTS_SECONDS = 10
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_SSL_REDIRECT = True
