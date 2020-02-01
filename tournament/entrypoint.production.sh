#!/bin/sh

set -e

python manage.py migrate
python manage.py collectstatic

# Set up a superuser if one doesn't already exist
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('test', '', 'test') if not User.objects.filter(username='test').count() else 1" | python manage.py shell


daphne -b 0.0.0.0 -p 8000 tournament.asgi:application -v 1
