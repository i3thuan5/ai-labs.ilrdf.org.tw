FROM python:3.12
WORKDIR /app

COPY requirements-prod.txt ./
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY autuan/ ./

ENV DJANGO_SETTINGS_MODULE=autuan.settings-tsiunnsuann

EXPOSE 8000
CMD python manage.py collectstatic --noinput && \
	gunicorn --workers 2 autuan.wsgi

# 問題二：不包RUN python manage.py migrate？https://forum.djangoproject.com/t/serving-django-static-files-in-nginx-docker/33969
# 問題三：發現不能用RUN python manage.py collectstatic --noinput
# 問題四：要能外連應該就是設定EXPOSE？