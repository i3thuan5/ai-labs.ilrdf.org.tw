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

SECURE_HSTS_SECONDS = 3600
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_HTTPONLY = True

# Wagtail

WAGTAILADMIN_BASE_URL = VIRTUAL_HOST[0]


CSRF_TRUSTED_ORIGINS = []
LANGUAGE_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

if os.getenv('TOX_CHECKDEPLOY', default=False):
    # 為著避免Multiple HSTS headers，
    # 所以下底這部份設定攏tī nginx-proxy做，
    # Django毋免做。
    SECURE_HSTS_SECONDS = 10
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# X_FRAME_OPTIONS = 'DENY'
# EMAIL_*
# ADMINS
# LOGGING

# 愛問的：
# SECURE_SSL_HOST
# FILE_UPLOAD_MAX_MEMORY_SIZE
