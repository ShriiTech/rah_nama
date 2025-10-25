import os
from pathlib import Path

# مسیر پایه پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

# پوشه‌ی لاگ‌ها
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    # --- فرمت خروجی لاگ‌ها ---
    "formatters": {
        "default": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        },
    },

    # --- هندلرها (جایی که لاگ نوشته می‌شود) ---
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "app.log",   # مسیر مطلق، نه relative
            "formatter": "default",
        },
    },

    # --- لاگر اصلی پروژه ---
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}
