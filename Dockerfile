FROM python:3.12
WORKDIR /app

ENV DJANGO_SETTINGS_MODULE=autuan.settings-tsiunnsuann

COPY requirements-prod.txt ./
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY autuan/ ./

EXPOSE 8000
COPY django_gunicorn_start.sh ./
RUN chmod +x django_gunicorn_start.sh
CMD ["./django_gunicorn_start.sh"]


# 問題二：看教典不包python manage.py migrate？
# 問題三：python manage.py collectstatic --noinput為啥物是run time才做，毋是build time？
# 日後按怎判斷？
