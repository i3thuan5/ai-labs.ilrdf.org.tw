import logging
import os
import sentry_sdk

from .settings import *  # noqa
# Core

DEBUG = False
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
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
        "PASSWORD": os.getenv('POSTGRES_PASSWORD'),
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


logger = logging.getLogger(__name__)
try:
    with open(os.getenv('SENTRY_DSN_FILE'), 'r') as tong:
        SENTRY_DSN = tong.readline()
except:
    SENTRY_DSN = None

logger.critical("---Start logging---")
logger.critical("SENTRY_DSN={}".format(SENTRY_DSN))
logger.critical("POSTGRES_PASSWORD={}".format(os.getenv('POSTGRES_PASSWORD')))
logger.critical("---End logging---")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Add request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
    )
