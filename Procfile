release: python manage.py compilestatic
release: python manage.py collectstatic --noinput
web: gunicorn Bnice.wsgi --log-file -