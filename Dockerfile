FROM python:3.12
WORKDIR /app

COPY requirements-prod.txt ./
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY autuan/ ./

ENV DJANGO_SETTINGS_MODULE=autuan.settings-tsiunnsuann

EXPOSE 80
CMD python manage.py collectstatic --noinput && \
	gunicorn --workers 2 autuan.wsgi

# 進度：collectstatic失敗
# PermissionError: [Errno 13] Permission denied: '/staticfiles'
# 問題二：不包RUN python manage.py migrate？
# 問題三：發現不能用RUN python manage.py collectstatic --noinput
