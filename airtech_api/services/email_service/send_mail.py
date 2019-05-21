from airtech_api.utils.constants import APP_EMAIL
from celery_config import celery_app
from django.template.loader import get_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os


@celery_app.task(name='send-email-to-user-as-html')
def send_mail_as_html(subject, receivers, html):
    """Sends mail as html

    Args:
        subject(str): The subject of the email
        receivers(list):  A list of emails of the receivers
        html(str): The html to be sent as a mail

    Returns:
        (str): Returns 'success' if the mail is sent successfully
    """

    message = Mail(from_email=APP_EMAIL,
                   to_emails=receivers,
                   subject=subject,
                   html_content=html)

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        sg.send(message)

    except Exception:
        return 'Failure'
    return 'Success'


def generate_html_from_template(name, data=None):
    """Returns html using a template data

    Args:s
        name(str): The name of the template
        data(dict): Data contain

    Returns:
        (str): String containing the html
    """
    template = get_template(name)
    return template.render(data)
