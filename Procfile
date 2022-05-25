web: gunicorn CSVFake.wsgi
worker: celery -A CSVFake.celery worker -B --loglevel=info
