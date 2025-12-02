import os
import sentry_sdk

from .settings import *  # noqa


def read_secret(secret_name):
    try:
        with open(os.getenv(secret_name), 'r') as tong:
            return tong.readline().rstrip()
    except IOError:
        return None


# Core

DEBUG = False

SECRET_KEY = read_secret('DJANGO_SECRET_KEY_FILE')
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOW_HOSTS').split(',')
CSRF_TRUSTED_ORIGINS = []
for host in ALLOWED_HOSTS:
    CSRF_TRUSTED_ORIGINS.append(f'https://{host}')

# Static Files

STATIC_ROOT = '/staticfiles/'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "postgres",
        "USER": "postgres",
        "PASSWORD": read_secret('POSTGRES_PASSWORD_FILE'),
        "HOST": "postgres",
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

WAGTAILADMIN_BASE_URL = ALLOWED_HOSTS[0]


if os.getenv('TOX_CHECKDEPLOY', default=False):
    # Django Deploy檢查有建議ài設定以下項目，
    # 因為下底設定實際上攏tī nginx-proxy做，
    # Django毋免做。
    # Django Deploy檢查ê時暫時先開--開。
    SECURE_HSTS_SECONDS = 10
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_SSL_REDIRECT = True


# Sentry

SENTRY_DSN = read_secret('SENTRY_DSN_FILE')

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=0.0,
        # Add request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
    )
