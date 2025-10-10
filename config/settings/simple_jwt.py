from datetime import timedelta
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")  # بارگذاری فایل .env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,          # refresh token چرخشی
    'BLACKLIST_AFTER_ROTATION': True,       # refresh token بلاک بعد از rotation
    'UPDATE_LAST_LOGIN': True,              # بروزرسانی آخرین login
    'ALGORITHM': 'HS256',                   # یا RS256 برای کلید عمومی/خصوصی
    'SIGNING_KEY': SECRET_KEY,              # از SECRET_KEY پروژه استفاده می‌کنه
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
