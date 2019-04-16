#!/usr/bin/env bash
echo "<<< API is now trying to connect to the database >>> "
echo "<<< Making migrations >>> "
python manage.py makemigrations
echo "<<< Migrating Database >>> "
python manage.py migrate # migrate db

sleep 2
echo "<<< Starting celery_config worker >>> "
exec celery -A  celery_config.celery_app worker --loglevel=info  & # runs celery_config worker

echo "<<< Feeling the beat by spinning up celery_config-beat >>> "
celery -A celery_config.celery_schedules beat --loglevel=info  & #runs celery_config beat
sleep 5
echo "<<< Waiting for the celery_config-workers to flow with the beat >>> "

echo "Starting server >>> "

echo "PORT = ${PORT}"
exec python manage.py runserver 0.0.0.0:$PORT

