#!/usr/bin/env bash

echo "API is sleeping for 30 seconds to allow Database to connect..."
sleep 30
echo "API is now trying to connect to the database..."
echo "Making migrations..."
python manage.py makemigrations
echo "Migrating Database..."
python manage.py migrate
echo "Starting server..."
exec python manage.py runserver 0.0.0.0:7000
