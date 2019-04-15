import os
import dotenv
dotenv.load_dotenv()

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_mail():

    message = Mail(
        from_email='airtech@example.com',
        to_emails='to@example.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content=
        '<strong>and easy to do anywhere, even with Python</strong>')
    try:
        import pdb
        pdb.set_trace()

        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
