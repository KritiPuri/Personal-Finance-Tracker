release: python manage.py migrate --noinput
web: gunicorn personalfinance.wsgi --bind 0.0.0.0:$PORT