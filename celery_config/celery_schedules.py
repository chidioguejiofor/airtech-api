from . import celery_scheduler
# from celery.schedules import crontab

celery_scheduler.conf.beat_schedule = {
    # This cronjob is used to test that celery_config is properly set up
    # It executes every 60 seconds
    'add-every-100-hours': {
        'task': 'add_number',
        'schedule': 6.0,
        'args': (16, 16)
    }
}
