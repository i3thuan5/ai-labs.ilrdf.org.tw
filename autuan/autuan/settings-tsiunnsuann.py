import os
from .settings import *  # noqa

DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY')

VIRTUAL_HOST = os.getenv('VIRTUAL_HOST').split(',')

ALLOWED_HOSTS = VIRTUAL_HOST
