from celery_config import celery_scheduler


@celery_scheduler.task(name='add_number')
def add_numbers(*args):
    return sum(args)
