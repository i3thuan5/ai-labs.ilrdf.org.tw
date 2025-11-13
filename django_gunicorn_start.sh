#!/bin/sh

# collect static files
python manage.py collectstatic --noinput

# start gunicorn server
gunicorn --workers 2 autuan.wsgi