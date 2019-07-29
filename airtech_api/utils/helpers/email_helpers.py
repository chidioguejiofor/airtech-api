# Create your views here.
from airtech_api.utils.helpers.json_helpers import generate_token
from airtech_api.services.email_service.send_mail import send_mail_as_html, generate_html_from_template
from datetime import datetime, timedelta


def send_email_with_token(email, file_name, redirect_url, **kwargs):
    confirm_link = kwargs.pop('confirm_link')
    mail_type = kwargs.pop('mail_type')
    template_data = kwargs

    token_data = {
        'email': email,
        'type': mail_type,
        'redirect_url': redirect_url,
        'exp': datetime.utcnow() + timedelta(minutes=5)
    }
    token = generate_token(token_data)
    html = generate_html_from_template(
        file_name, {
            **template_data,
            'confirm_link': confirm_link + f'/{token}',
        })
    # import  pdb; pdb.set_trace()
    send_mail_as_html.delay(template_data['subject'], [email], html)
