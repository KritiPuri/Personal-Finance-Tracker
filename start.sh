#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn personalfinance.wsgi --bind 0.0.0.0:$PORT