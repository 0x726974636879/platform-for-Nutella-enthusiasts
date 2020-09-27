#!/bin/sh

pip install -r /usr/src/app/requirements.txt

python /usr/src/app/src/manage.py runserver 0:8000 --settings=settings.base

exec "$@"