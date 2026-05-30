# =============================================================
#  settings.py — настройки Django-проекта
# =============================================================
#  Этот файл определяет, как именно Django запускает и работает с
#  нашим сайтом: путь к БД, установленные приложения, middleware,
#  шаблоны, статика, локализация и т.д.
# =============================================================

import os
from pathlib import Path

# BASE_DIR — абсолютный путь к корню проекта (где лежит manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY — секрет, которым Django подписывает сессии и токены.
# В продакшене берётся из переменной окружения (Render задаёт её сам).
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-ulsk-it-internships-2025-secret-key-change-in-production',
)

# DEBUG=True — режим разработки. В продакшене (на Render) выключается
# через переменную окружения DEBUG=False (значение по умолчанию здесь — False).
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('1', 'true', 'yes')

# ALLOWED_HOSTS — список доменов, с которых сайт принимает запросы.
ALLOWED_HOSTS = ['*']

# Render отдаёт публичный домен через эту переменную — добавляем его
# в доверенные источники для CSRF (нужно для отправки форм по HTTPS).
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

# INSTALLED_APPS — список «приложений» (модулей) Django.
# Первые 6 — встроенные: админка, авторизация, сессии, сообщения,
# обработка статики. Последнее — наше приложение internships
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'internships',                  # наше приложение
]

# MIDDLEWARE — цепочка обработчиков, через которые проходит каждый
# запрос и ответ. Порядок важен: сначала security и session,
# в конце clickjacking (X-Frame-Options)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',                  # HTTPS, HSTS и т.д.
    'whitenoise.middleware.WhiteNoiseMiddleware',                     # отдача статики в продакшене
    'django.contrib.sessions.middleware.SessionMiddleware',           # сессии в cookie
    'django.middleware.common.CommonMiddleware',                      # базовые проверки URL
    'django.middleware.csrf.CsrfViewMiddleware',                      # защита от CSRF-атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',        # подгружает request.user
    'django.contrib.messages.middleware.MessageMiddleware',           # всплывающие уведомления
    'django.middleware.clickjacking.XFrameOptionsMiddleware',         # защита от clickjacking
]

# Главный файл маршрутов проекта
ROOT_URLCONF = 'ulsk_internships.urls'

# Настройки системы шаблонов (HTML)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],                  # дополнительные папки шаблонов (помимо app/templates/)
        'APP_DIRS': True,            # искать в каждом приложении папку templates/
        'OPTIONS': {
            # context_processors — функции, добавляющие переменные во все шаблоны
            # (например, {{ user }} в любой шаблон)
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Точка входа WSGI-сервера (Gunicorn в продакшене)
WSGI_APPLICATION = 'ulsk_internships.wsgi.application'

# База данных.
# На Render база подключается через одну переменную DATABASE_URL
# (её автоматически задаёт render.yaml). Локально, если DATABASE_URL
# не задана, используется PostgreSQL с параметрами по умолчанию.
import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('PG_NAME',     'ulsk_internships'),
            'USER': os.environ.get('PG_USER',     'postgres'),
            'PASSWORD': os.environ.get('PG_PASSWORD', '12345'),
            'HOST': os.environ.get('PG_HOST',     'localhost'),
            'PORT': os.environ.get('PG_PORT',     '5432'),
        }
    }

# Валидаторы паролей при регистрации.
# 1) пароль не похож на логин/имя; 2) не короче 8; 3) не из топ-распространённых;
# 4) не состоит только из цифр
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Локализация
LANGUAGE_CODE = 'ru'                # русский язык интерфейса админки
TIME_ZONE = 'Europe/Ulyanovsk'      # часовой пояс
USE_I18N = True                     # включить переводы
USE_TZ = True                       # хранить даты в UTC, отображать в местном поясе

# Статические файлы (CSS, JS, картинки разработчика)
STATIC_URL = '/static/'                          # URL, по которому отдаются статические файлы
STATICFILES_DIRS = [BASE_DIR / 'static']         # где искать статику в разработке
STATIC_ROOT = BASE_DIR / 'staticfiles'           # куда collectstatic положит файлы для продакшена

# WhiteNoise: сжимает статику и отдаёт её прямо из Django в продакшене
# (на Render нет отдельного nginx), с кэширующими заголовками.
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

# Медиа-файлы (загружаемые пользователем: лого, резюме, картинки стажировок)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# URL для входа (туда перенаправит @login_required, если пользователь не залогинен)
LOGIN_URL = '/login/'
# Куда отправлять пользователя после успешного входа
LOGIN_REDIRECT_URL = '/'

# Тип первичного ключа по умолчанию для новых моделей (BigInt, до 9 квинтиллионов)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
