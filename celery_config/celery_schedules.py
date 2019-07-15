from . import celery_scheduler
from celery.schedules import crontab

celery_scheduler.conf.beat_schedule = {
    # This cronjob is used to test that celery_config is properly set up
    # It executes every 60 seconds
    # 'notify-user-of-bookings-about-to-expired-every-12-hours': {
    #     'task': 'add_number',
    #     'schedule':crontab(hour='0,12,18'),
    # }
}
