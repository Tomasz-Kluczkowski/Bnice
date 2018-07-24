release: python manage.py compilestatic
release: python manage.py collectstatic --noinput --clear
web: gunicorn Bnice.wsgi --log-file -