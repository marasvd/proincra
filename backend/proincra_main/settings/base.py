# backend/core/settings/base.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Carga .env en runtime (si existe)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOTENV_PATH = BASE_DIR / '.env'
if DOTENV_PATH.exists():
    load_dotenv(DOTENV_PATH)

# Seguridad
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('1', 'true', 'yes')

# Hosts y CORS (lista simple en dev)
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()]

# Aplicaciones mínimas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceros
    'rest_framework',

    # Apps del proyecto
    'app.gestion_usuarios',   # Usuarios y roles (MVP)
    'app.proyectos_core',     # Beneficiarios y Avances (MVP)
    'app.beneficiarios_app',  # placeholder / futuro microservicio
    'app.inventario_app',
    'app.contabilidad_app',
    'app.auditoria_app',
    'app.contratacion_app',
    'app.facturacion_app',
    'app.proveedores_app',
    'app.cartera_app',
    'app.nomina_app',
    'app.compras_app',
    'app.operaciones_ti_app',
    'app.tesoreria_app', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'proincra_main.urls'  # ajusta según tu proyecto

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.parent / 'frontend' / 'templates',  # Apunta al frontend
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # si añadiste contexto de modulos:
                'app.gestion_usuarios.context_processors.modulos_disponibles',
            ],
        },
    },
]

WSGI_APPLICATION = 'proincra_main.wsgi.application'  # ajusta si tu módulo se llama distinto

# Autenticación
AUTH_USER_MODEL = os.getenv('AUTH_USER_MODEL', 'gestion_usuarios.Actor')

# Internacionalización
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static / Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Aquí le decimos explícitamente dónde buscar archivos estáticos en desarrollo
STATICFILES_DIRS = [
    BASE_DIR.parent / 'frontend' / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# Logging simple (ajusta en prod)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
}

# DRF (config básica)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        # en prod agregar JWT o token
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
