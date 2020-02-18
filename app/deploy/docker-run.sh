#!/usr/bin/env bash
set -u   # crash on missing env variables
set -e   # stop on any error
set -x

echo Collecting static files
python manage.py collectstatic --settings settings.settings --no-input
# python manage.py migrate settings.settings --noinput

ls -al /static/

chmod -R 777 /static

exec uwsgi
