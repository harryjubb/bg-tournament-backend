#!/bin/sh

set -e

python manage.py migrate

# Set up a superuser if one doesn't already exist
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('test', '', 'test') if not User.objects.filter(username='test').count() else 1" | python manage.py shell

echo "Running in development with runserver"
python manage.py runserver 0.0.0.0:8000
