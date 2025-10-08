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

# Create necessary directories AS ROOT
RUN mkdir -p /app/logs /app/static /app/media \
    && mkdir -p /app/apps/catalog/migrations/ /app/account/migrations/ \
    && touch /app/apps/catalog/migrations/__init__.py \
    && touch /app/account/migrations/__init__.py

# Copy and install Python dependencies AS ROOT
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files AS ROOT
COPY . .

# Copy entrypoint and start scripts and make them executable AS ROOT
COPY entrypoint.sh /entrypoint.sh
COPY start.sh /app/start.sh
RUN chmod +x /entrypoint.sh /app/start.sh

# Give ownership of /app to appuser (optional if you want to run as non-root later)
RUN chown -R appuser:appuser /app /entrypoint.sh /app/start.sh

# Switch to root to avoid permission issues
USER root

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
