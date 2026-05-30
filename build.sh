#!/usr/bin/env bash
# Скрипт сборки, который Render запускает при каждом деплое.
set -o errexit   # упасть при любой ошибке

# 1. Зависимости
pip install -r requirements.txt

# 2. Собрать статику (CSS/JS/картинки) в STATIC_ROOT для WhiteNoise
python manage.py collectstatic --no-input

# 3. Применить миграции БД
python manage.py migrate

# 4. Привести базу к состоянию дампа: очистить и загрузить site_data.json.
#    flush удаляет ВСЕ данные (схему оставляет), затем loaddata заливает
#    наши реальные записи с логотипами. Так на Render не остаётся мусора
#    от прежних seed-скриптов (лишние компании/стажировки вроде «Контек-Софт»).
echo "Очищаю базу и загружаю данные из site_data.json..."
python manage.py flush --no-input
python manage.py loaddata site_data.json

# 5. Создать суперпользователя для /admin/, если его ещё нет
#    (использует переменные DJANGO_SUPERUSER_* из окружения)
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
U = get_user_model()
u = os.environ.get('DJANGO_SUPERUSER_USERNAME')
p = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
e = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
if u and p and not U.objects.filter(username=u).exists():
    U.objects.create_superuser(u, e, p)
    print('Суперпользователь создан:', u)
else:
    print('Суперпользователь уже есть или переменные не заданы.')
"
