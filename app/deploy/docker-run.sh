#!/usr/bin/env bash
# set -u   # crash on missing env variables
set -e   # stop on any error
set -x

#cp /app/nginx/vhost.conf /etc/nginx/sites-enabled/
#chmod 777 /etc/nginx/sites-enabled/vhost.conf
# rm /etc/nginx/sites-enabled/default.conf

python manage.py collectstatic --settings settings.settings --no-input
python manage.py migrate --settings settings.settings --no-input

if [ -n "${ADMIN_USERNAME}" ] && [ -n "${ADMIN_PASSWORD}" ]; then
  python manage.py initadmin --settings settings.settings --username $ADMIN_USERNAME --password $ADMIN_PASSWORD
fi

chmod -R 777 /static

echo "Test nginx"
nginx -t


echo "Start nginx"
/etc/init.d/nginx start

exec uwsgi uwsgi.ini

