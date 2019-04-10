from django.conf import settings
from celery import Celery
from airtech_api.utils.constants import CELERY_TASKS
import os
import dotenv
dotenv.load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airtech_api.settings.base')

REDIS_SERVER_URL = os.getenv('REDIS_SERVER_URL', 'redis://localhost')
print('REDIS_SERVER_URL = {}'.format(REDIS_SERVER_URL))
celery_app = Celery(__name__, broker=REDIS_SERVER_URL, include=CELERY_TASKS)
celery_app.config_from_object('django.conf.settings')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

celery_scheduler = Celery(__name__, broker=REDIS_SERVER_URL)
celery_scheduler.conf.enable_utc = False
