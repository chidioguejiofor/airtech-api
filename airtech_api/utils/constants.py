FIELD_IS_REQUIRED_STR = 'This field is required.'
DEFAULT_ITEMS_PER_PAGE = '10'
CELERY_TASKS = [
    'airtech_api.services.email_service.send_mail_helpers',
]
