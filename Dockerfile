FROM python:3.12

ENV DJANGO_SETTINGS_MODULE=autuan.settings-tsiunnsuann

WORKDIR /app
COPY requirements-prod.txt ./
RUN pip install --no-cache-dir -r requirements-prod.txt

RUN addgroup --gid 1000 nonroot && \
    adduser --uid 1000 --disabled-password --ingroup nonroot --quiet nonroot
USER nonroot

COPY autuan/ ./

EXPOSE 8000
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", "autuan.wsgi"]
