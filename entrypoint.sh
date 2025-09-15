#!/bin/bash
set -e

LOG_FILE="/app/logs/docker_entrypoint.log"

# Create logs directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "🚀 Starting container initialization..."

# ===== Step 1: Database Connection Check =====
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${POSTGRES_DB:-rah_nama}
DB_USER=${POSTGRES_USER:-postgres}
DB_PASSWORD=${POSTGRES_PASSWORD:-44139890}

log "⏳ Waiting for database ($DB_HOST:$DB_PORT) to be ready..."

# Enhanced database check with timeout
MAX_TRIES=60
TRIES=0

while [ $TRIES -lt $MAX_TRIES ]; do
    if nc -z "$DB_HOST" "$DB_PORT"; then
        log "✅ Database port is open!"
        
        # Additional check: try to connect to PostgreSQL
        if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" >/dev/null 2>&1; then
            log "✅ Database connection successful!"
            break
        else
            log "❗ Database port is open but connection failed. Retrying..."
        fi
    else
        log "❗ Database not ready yet. Attempt $((TRIES + 1))/$MAX_TRIES"
    fi
    
    TRIES=$((TRIES + 1))
    sleep 1
done

if [ $TRIES -eq $MAX_TRIES ]; then
    log "❌ Database connection timeout after $MAX_TRIES attempts"
    exit 1
fi

# ===== Step 2: Django Setup Check =====
log "🔧 Checking Django setup..."

# Verify Django can import settings
if ! python -c "import django; django.setup()" 2>&1 | tee -a "$LOG_FILE"; then
    log "❌ Django setup failed!"
    exit 1
fi

log "✅ Django setup successful!"

# ===== Step 3: Collect Static Files (if needed) =====
if [ "${DJANGO_COLLECT_STATIC:-true}" = "true" ]; then
    log "📦 Collecting static files..."
    if python manage.py collectstatic --noinput --clear 2>&1 | tee -a "$LOG_FILE"; then
        log "✅ Static files collected successfully."
    else
        log "⚠️ Static files collection failed, but continuing..."
    fi
fi

# ===== Step 4: Create Migrations =====
log "📦 Creating migrations for main apps..."

# Create migrations for the main project
if python manage.py makemigrations --verbosity=2 2>&1 | tee -a "$LOG_FILE"; then
    log "✅ Main makemigrations completed successfully."
else
    log "❌ Main makemigrations failed!"
    exit 1
fi

# Create migrations for account app specifically
log "📦 Creating migrations for account app..."
if python manage.py makemigrations account --verbosity=2 2>&1 | tee -a "$LOG_FILE"; then
    log "✅ Account app migrations created successfully."
else
    log "⚠️ Account app migrations failed, but continuing..."
fi

# Create migrations for catalog app if it exists
if [ -d "/app/apps/catalog" ]; then
    log "📦 Creating migrations for catalog app..."
    if python manage.py makemigrations catalog --verbosity=2 2>&1 | tee -a "$LOG_FILE"; then
        log "✅ Catalog app migrations created successfully."
    else
        log "⚠️ Catalog app migrations failed, but continuing..."
    fi
fi

# ===== Step 5: Show Migration Plan =====
log "📋 Checking migration plan..."
if python manage.py showmigrations --plan 2>&1 | tee -a "$LOG_FILE"; then
    log "✅ Migration plan displayed."
else
    log "⚠️ Could not display migration plan, but continuing..."
fi

# ===== Step 6: Apply Migrations =====
log "⚙️ Applying migrations..."
if python manage.py migrate --verbosity=2 2>&1 | tee -a "$LOG_FILE"; then
    log "✅ Migrations applied successfully."
else
    log "❌ Migration failed!"
    exit 1
fi

# ===== Step 7: Create Superuser (optional) =====
if [ "${CREATE_SUPERUSER:-false}" = "true" ] && [ -n "${DJANGO_SUPERUSER_USERNAME}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD}" ]; then
    log "👤 Creating superuser..."
    if python manage.py createsuperuser --noinput 2>&1 | tee -a "$LOG_FILE"; then
        log "✅ Superuser created successfully."
    else
        log "⚠️ Superuser creation failed (might already exist)."
    fi
fi

# ===== Step 8: Additional Setup Commands =====
# Load fixtures if specified
if [ -n "${DJANGO_FIXTURES}" ]; then
    log "📊 Loading fixtures: $DJANGO_FIXTURES"
    for fixture in $DJANGO_FIXTURES; do
        if python manage.py loaddata "$fixture" 2>&1 | tee -a "$LOG_FILE"; then
            log "✅ Fixture $fixture loaded successfully."
        else
            log "⚠️ Failed to load fixture $fixture."
        fi
    done
fi

log "🎉 Container initialization completed successfully!"
log "🚀 Starting application with command: $*"

# ===== Step 9: Execute the main command =====
exec "$@"