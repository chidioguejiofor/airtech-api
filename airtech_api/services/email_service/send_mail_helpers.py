from . import DOMAIN_NAME, PASSWORD
import smtplib
from email.mime.text import MIMEText
from celery_config import celery_app
from django.template.loader import get_template


@celery_app.task(name='send-email-to-user-as-html')
def send_mail_as_html(subject, receiver, html):
    """Sends mail as html

    Args:
        subject(str): The subject of the email
        receiver(str):  The email of the receiver
        html(str): The html to be sent as a mail

    Returns:
        (str): Returns 'success' if the mail is sent successfully
    """
    mime_object = MIMEText(html, 'html')
    mime_object['Subject'] = subject
    mime_object['From'] = f"Airtech API <foo@{DOMAIN_NAME}>"
    mime_object['To'] = receiver
    smtp_object = smtplib.SMTP('smtp.mailgun.org', 587)
    smtp_object.login(f'postmaster@{DOMAIN_NAME}', PASSWORD)
    smtp_object.sendmail(mime_object['From'], mime_object['To'],
                         mime_object.as_string())
    smtp_object.quit()
    return 'Success'


def generate_html_from_template(name, data=None):
    """Returns html using a template data

    Args:
        name(str): The name of the template
        data(dict): Data contain

    Returns:
        (str): String containing the html
    """
    template = get_template(name)
    return template.render(data)
