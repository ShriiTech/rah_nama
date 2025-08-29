#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e


# Run database migrations
echo "Applying database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput


# Start the server
echo "Starting server..."
exec "$@"
