import os
from .settings import *  # noqa

DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY')

VIRTUAL_HOST = os.getenv('VIRTUAL_HOST').split(',')

ALLOWED_HOSTS = VIRTUAL_HOST

# Static Files

STATIC_ROOT = '/staticfiles/'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mypostgres',
        "USER": "mydatabaseuser",
        "PASSWORD": "3a2@)5b=4a9b*C28^dD9FG",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# Security

SECURE_HSTS_SECONDS = 3600
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_AGE =
CSRF_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = # 文件指出愛符合三要件才設定這
SECURE_SSL_REDIRECT = True
# SECURE_SSL_HOST
SESSION_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_SECURE = True

# Wagtail

WAGTAILADMIN_BASE_URL = VIRTUAL_HOST[0]
