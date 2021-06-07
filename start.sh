#! /usr/bin/env bash

./manage.py collectstatic --no-input
./manage.py migrate
gunicorn opensplit.wsgi --bind 0.0.0.0:8000
