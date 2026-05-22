#!/bin/sh
set -e

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Loading demo data (if database is empty)..."
python manage.py load_demo_data

echo "Creating superuser (if env vars set and user doesn't exist)..."
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" \
        2>/dev/null || echo "Superuser already exists, skipping."
fi

echo "Ensuring media files exist..."
python manage.py load_demo_data --ensure-images

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn RealEstateAgency.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-2}" \
    --timeout 120
