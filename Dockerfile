# استفاده از python:3.11-slim به عنوان base image
FROM python:3.11-slim

# تنظیمات محیط
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# نصب پیش‌نیازهای سیستم
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# ساخت کاربر غیر-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# پوشه کاری
WORKDIR /app

# کپی requirements
COPY requirements.txt .

# نصب پکیج‌های Python
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# کپی کل پروژه
COPY . .

# ساخت پوشه migrations و دادن دسترسی کامل
RUN mkdir -p /app/apps/catalog/migrations/ \
    && chown -R root:root /app \
    && chmod -R 777 /app

# کپی entrypoint و دادن دسترسی
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
    && chown root:root /entrypoint.sh

# استفاده از root برای اطمینان از دسترسی کامل
USER root

# باز کردن پورت
EXPOSE 8000

# health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/', timeout=10)" || exit 1

# entrypoint برای اجرای اسکریپت
ENTRYPOINT ["/entrypoint.sh"]

# دستور پیش‌فرض
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
