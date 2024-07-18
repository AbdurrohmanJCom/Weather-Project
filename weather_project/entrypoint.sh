#!/usr/bin/env bash
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo $DEBUG
if [ "$DEBUG" = "True" ]; then
  echo "if"
  # Development configuration with hot reloading
  exec python manage.py runserver 0.0.0.0:8000
else
  echo "Else"
  # Production configuration
  exec gunicorn --reload -b 0.0.0.0:8000 logist.wsgi --workers 5 --timeout 300 --graceful-timeout 10 --log-level warning
fi

exec "$@"