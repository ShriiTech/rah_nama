# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        postgresql-client \
        netcat-openbsd \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create application user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set work directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/logs /app/static /app/media \
    && chown -R appuser:appuser /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY . .

# Create migrations directory with proper permissions
RUN mkdir -p /app/apps/catalog/migrations/ /app/account/migrations/ \
    && touch /app/apps/catalog/migrations/__init__.py \
    && touch /app/account/migrations/__init__.py

# Copy entrypoint script and start script, make them executable
COPY entrypoint.sh /entrypoint.sh
COPY start.sh /app/start.sh
RUN chmod +x /entrypoint.sh /app/start.sh

# Set ownership of the app directory to appuser
RUN chown -R appuser:appuser /app /entrypoint.sh

# Switch to non-root user for security
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]