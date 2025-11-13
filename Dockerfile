FROM python:3.12
WORKDIR /app

ENV DJANGO_SETTINGS_MODULE=autuan.settings-tsiunnsuann

COPY requirements-prod.txt ./
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY autuan/ ./

EXPOSE 8000

CMD ["gunicorn", "--workers", "2", "autuan.wsgi"]