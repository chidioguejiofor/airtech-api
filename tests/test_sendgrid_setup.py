# Third Party Libraries
import pytest

from airtech_api.services.email_service.send_mail import send_mail_as_html

from unittest.mock import Mock
from sendgrid import SendGridAPIClient


@pytest.mark.django_db
class TestSendGridSetup:
    """
    Tests the SendGridSetup
    """

    def test_when_a_connection_cannot_be_established_fails(self):
        """Should return "Failure" when the connection cannot be made


        Returns:
            None
        """
        send_mail_as_html.delay = Mock(side_effect=send_mail_as_html)
        SendGridAPIClient.send = Exception('Email Cannot be connected to')

        result = send_mail_as_html.delay('Any', 'is', 'fine')
        assert result == 'Failure'

    def test_when_a_connection_is_send_to_mail_succeeds(self, client):
        """Should return a welcome message to the user on GET /api


        Returns:
            None
        """
        send_mail_as_html.delay = Mock(side_effect=send_mail_as_html)
        SendGridAPIClient.send = Mock(return_value='')

        result = send_mail_as_html.delay('Any', 'is', 'fine')
        assert result == 'Success'
