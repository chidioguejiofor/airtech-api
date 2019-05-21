# Create your views here.

from airtech_api.utils.helpers.json_helpers import generate_token
from airtech_api.services.email_service.send_mail import send_mail_as_html, generate_html_from_template

from ..constants import CONFIRM_EMAIL_TYPE, CONFRIM_EMAIL_SUBJECT
from datetime import datetime, timedelta


def send_confirm_mail(email, server_host, client_host):
    """Sends a confirmation email to a user

    Args:
        email (str): a string containing the email of the recipients
        server_host: The server host name of the server
        client_host: The host name of the client

    """
    token_data = {
        'email': email,
        'type': CONFIRM_EMAIL_TYPE,
        'redirect_url': 'http://{}/login'.format(client_host),
        'exp': datetime.utcnow() + timedelta(minutes=5)
    }
    token = generate_token(token_data)
    html = generate_html_from_template(
        'confirm-email.html', {
            'confirm_link':
            'http://{}/api/v1/auth/confirm-email/{}'.format(
                server_host, token)
        })

    send_mail_as_html.delay(CONFRIM_EMAIL_SUBJECT, [email], html)
