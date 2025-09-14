#!/bin/bash
set -e

LOG_FILE="/app/docker_entrypoint.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "🚀 Starting container initialization..."

# اطمینان از وجود پوشه migrations
log "📂 Checking migrations directory..."
mkdir -p /app/apps/catalog/migrations/
chmod -R 777 /app/apps/catalog/migrations/

# اجرای makemigrations
log "📦 Running makemigrations..."
if python manage.py makemigrations --noinput 2>&1 | tee -a "$LOG_FILE"; then
    log "✅ makemigrations completed successfully."
else
    log "❌ makemigrations failed!"
    exit 1
fi

# اجرای migrate
log "⚙️ Running migrate..."
if python manage.py migrate --noinput 2>&1 | tee -a "$LOG_FILE"; then
    log "✅ migrate completed successfully."
else
    log "❌ migrate failed!"
    exit 1
fi

log "🎉 All migrations done! Starting Django server..."

# اجرای دستور پیش‌فرض Dockerfile (مثل runserver)
exec "$@"
