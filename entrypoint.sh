#!/bin/sh
set -e

echo "Aplicando migrations..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
exec gunicorn paineis_bi.wsgi:application \
    --bind 0.0.0.0:8002 \
    --workers 3 \
    --timeout 120
