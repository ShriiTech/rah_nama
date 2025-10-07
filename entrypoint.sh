#!/bin/bash
set -e

# Function to wait for PostgreSQL
wait_for_postgres() {
  echo "Waiting for PostgreSQL at $1..."
  until PGPASSWORD=$POSTGRES_PASSWORD pg_isready -h "$1" -U "$POSTGRES_USER"; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 2
  done
  echo "PostgreSQL is up and running!"
}

# Execute database migrations in a safe order
run_migrations() {
  echo "Making migrations if needed..."
  python manage.py makemigrations account
  python manage.py makemigrations

  echo "Applying database migrations in a safe order..."

  python manage.py migrate --noinput
}

# If postgres is specified as the first argument, extract the hostname
if [[ $1 == postgres* ]]; then
  postgres_host="${DB_HOST:-postgres}"
  shift
  wait_for_postgres "$postgres_host"
fi

# Handle tasks only for the WSGI container
if [[ "$(hostname)" == *"wsgi"* || "$@" == *"wsgi"* || "$@" == *"gunicorn"* || "$@" == *"runserver"* ]]; then
  # Create static directory if it doesn't exist
  mkdir -p /app/static

  # Apply migrations and create superuser only in the WSGI container
  run_migrations
fi

# Execute the CMD
echo "Starting service with command: $@"
exec "$@"
