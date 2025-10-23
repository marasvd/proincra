# backend/core/settings/dev.py
from .base import *

# Forzar modo desarrollo
DEBUG = True
ALLOWED_HOSTS = ['*']

# Use SQLite en desarrollo si NO se solicita Postgres
USE_POSTGRES = os.getenv('USE_POSTGRES', 'False').lower() in ('1','true','yes')
if USE_POSTGRES:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('DB_HOST', 'db'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Debug toolbar u otras utilidades (opcional)
INSTALLED_APPS += [
    # 'debug_toolbar',
]

# CORS (si tienes frontend local)
CORS_ALLOWED_ORIGINS = [
    os.getenv('FRONTEND_URL', 'http://localhost:3000'),
]
