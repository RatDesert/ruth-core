#!/usr/bin/env bash
cd src
python manage.py makemigrations user jwt_auth hub sensor
python manage.py migrate

gunicorn wsgi -b 0.0.0.0:8000
