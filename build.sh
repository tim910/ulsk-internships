#!/usr/bin/env bash
# Скрипт сборки, который Render запускает при каждом деплое.
set -o errexit   # упасть при любой ошибке

# 1. Зависимости
pip install -r requirements.txt

# 2. Собрать статику (CSS/JS/картинки) в STATIC_ROOT для WhiteNoise
python manage.py collectstatic --no-input

# 3. Применить миграции БД
python manage.py migrate

# 4. Наполнить демо-данными ОДИН раз — только если база ещё пустая.
#    (seed_data.py очищает и пересоздаёт данные, поэтому повторно не запускаем.)
if python manage.py shell -c "import sys; from internships.models import Internship; sys.exit(0 if Internship.objects.exists() else 1)"; then
    echo "Данные уже есть — пропускаю наполнение."
else
    echo "База пустая — наполняю демо-данными..."
    python manage.py shell < seed_data.py || true
    python manage.py shell < seed_more.py || true
fi

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
