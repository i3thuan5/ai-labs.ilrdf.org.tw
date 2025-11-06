FROM python:3.12
WORKDIR /app

COPY requirements-prod.txt ./
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY autuan/ ./
RUN python manage.py collectstatic --noinput

EXPOSE 80
ENV DJANGO_SETTINGS_MODULE=autuan.settings-tsiunnsuann
CMD ["gunicorn", \
	"--workers", "2", \
	"autuan.wsgi"]

# 進度：collectstatic失敗
# PermissionError: [Errno 13] Permission denied: '/staticfiles'