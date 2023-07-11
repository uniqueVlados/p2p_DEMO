"""Django settings for the project."""
import os

from environs import Env
from loguru import logger
from pathlib import Path


env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django_eventstream',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'users.apps.UsersConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'simple_history',
    'corsheaders',
    'constance',
    'role_permissions',
    'finances',
    'utils',
    'encryption',
    'btasks',
    'qiwi',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE = [
    'django_grip.GripMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'core.middlewares.CorsHeadersMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

if DEBUG:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'
ASGI_APPLICATION = 'project.asgi.application'

DATABASES = {"default": env.dj_db_url("DB_URL")}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates/static'),
]

MEDIA_URL = 'uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

if DEBUG:
    INTERNAL_IPS = ALLOWED_HOSTS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
HOST = env.str('HOST')
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')

# LOGGING

LOGS_PATH = os.path.join(BASE_DIR, 'logs', 'main.logs')

logger.add(LOGS_PATH, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

# Время жизни токена
TOKEN_EXPIRED_AFTER_HOURS = 12

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'users.permissions.AllowOptionsAuthentication',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.ExpiringTokenAuthentication',
    ]
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Хранилище уведомлений
EVENTSTREAM_STORAGE_CLASS = 'django_eventstream.storage.DjangoModelStorage'

SECURE_CROSS_ORIGIN_OPENER_POLICY = None

# ID счёта, на который зачисляются все комиссионные сборы
SYSTEM_ACCOUNT_ID = env.int('SYSTEM_ACCOUNT_ID')

# Настройки для лимитов банковских карт
CARD_TURNOVER_LIMIT = env.int('CARD_TURNOVER_LIMIT')
CARD_TURNOVER_BOUNDARY_LIMIT = env.int('CARD_TURNOVER_BOUNDARY_LIMIT')
CARD_TURNOVER_PERIOD = env.int('CARD_TURNOVER_PERIOD')
CARD_VACATION_PERIOD = env.int('CARD_VACATION_PERIOD')

# Метод шифрования для HMAC
HMAC_DIGESTMOD = env.str('HMAC_DIGESTMOD')

# Celery Configuration Options
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND')

# CORS headers
CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS')
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')

# URLs для форм пополнения и списания
URL_REPLENISH = env.str('URL_REPLENISH')
URL_WITHDRAW = env.str('URL_WITHDRAW')


# Настройки периодических фоновых задач
CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# QIWI

QIWI_HOST = env.str('QIWI_HOST')
QIWI_EDGE_HOST = env.str('QIWI_EDGE_HOST')
QIWI_PUBLIC_KEY = env.str('QIWI_PUBLIC_KEY')
QIWI_TOKEN = env.str('QIWI_TOKEN')
QIWI_TURNOVER_LIMIT = env.int('QIWI_TURNOVER_LIMIT')
QIWI_TURNOVER_BOUNDARY_LIMIT = env.int('QIWI_TURNOVER_BOUNDARY_LIMIT')
QIWI_TURNOVER_PERIOD = env.int('QIWI_TURNOVER_PERIOD')
QIWI_VACATION_PERIOD = env.int('QIWI_VACATION_PERIOD')
QIWI_PAYMENT_TIME = env.int('QIWI_PAYMENT_TIME')


# минимальная сумма транзакции, руб
MIN_TRANSACTION_AMOUNT = env.int('MIN_TRANSACTION_AMOUNT')


# Финансовые настройки
# Настройки динамической конфигурации
CONSTANCE_CONFIG = {
    'COMISSION': (0.04, 'Комиссия системы', float),
    }

# CSRF options
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')

SESSION_COOKIE_DOMAIN = 'dekafinance.ru'
