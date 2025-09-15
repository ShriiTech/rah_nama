#!/bin/bash
set -e

echo "🚀 Starting Django application..."

# Wait for database
echo "⏳ Waiting for database..."
python << END
import os
import time
import psycopg2
from psycopg2 import OperationalError

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'db'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('POSTGRES_DB', 'rah_nama'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', '44139890')
        )
        conn.close()
        print("✅ Database is ready!")
        break
    except OperationalError:
        retry_count += 1
        print(f"❗ Database not ready, retrying... ({retry_count}/{max_retries})")
        time.sleep(1)

if retry_count >= max_retries:
    print("❌ Database connection timeout!")
    exit(1)
END

# Create migrations
echo "📦 Creating migrations..."
python manage.py makemigrations --noinput

echo "📦 Creating migrations for account app..."
python manage.py makemigrations account --noinput

# Apply migrations
echo "⚙️ Applying migrations..."
python manage.py migrate --noinput

# Create superuser if environment variables are set
if [ "${CREATE_SUPERUSER:-false}" = "true" ] && [ -n "${DJANGO_SUPERUSER_USERNAME}" ]; then
    echo "👤 Creating superuser..."
    python manage.py createsuperuser --noinput || echo "⚠️ Superuser might already exist"
fi

# Collect static files if enabled
if [ "${DJANGO_COLLECT_STATIC:-false}" = "true" ]; then
    echo "📦 Collecting static files..."
    python manage.py collectstatic --noinput --clear
fi

echo "🎉 Setup completed! Starting Django server..."

# Start the Django development server
exec python manage.py runserver 0.0.0.0:8000