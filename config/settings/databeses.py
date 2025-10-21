# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv("POSTGRES_DB"),
#         'USER': os.getenv("POSTGRES_USER"),
#         'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
#         'HOST': os.getenv("DB_HOST"),
#         'PORT': os.getenv("DB_PORT"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rah_nama',
        'USER': 'postgres',
        'PASSWORD': '44139890',
        'HOST': 'db',
        'PORT': 5432,
    }
}
