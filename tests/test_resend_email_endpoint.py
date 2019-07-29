# Third Party Libraries
import pytest

from tests.helpers.assertion_helpers import assert_send_mail_data
from airtech_api.utils.constants import CONFRIM_EMAIL_SUBJECT
from airtech_api.utils import success_messages, error_messages
from airtech_api.services.email_service.send_mail import send_mail_as_html
from unittest.mock import Mock
from sendgrid import SendGridAPIClient

RESEND_EMAIL_ENDPOINT = '/api/v1/auth/resend-email'


@pytest.mark.django_db
class TestResendEmailRoute:
    """
    Tests the confirm email route
    """

    def test_resend_email_with_unverified_user_succeeds(
            self, client, saved_valid_user_one, valid_user_one_token):
        """Should fail when the token is expired

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one (model): a model that represents a user in the db
        """
        send_mail_as_html.delay = Mock(side_effect=send_mail_as_html)
        SendGridAPIClient.send = Mock(side_effect=lambda x: None)

        request_data = {
            'email': saved_valid_user_one.email,
            'callbackURL': 'https://test.com',
        }
        response = client.post(
            RESEND_EMAIL_ENDPOINT,
            data=request_data,
            HTTP_AUTHORIZATION=f'Bearer {valid_user_one_token}')
        response_data = response.data

        assert response.status_code == 200
        assert response_data['message'] == success_messages[
            'confirm_mail'].format(request_data['email'])
        assert response_data['status'] == 'success'
        message_obj = SendGridAPIClient.send.call_args[0][0]
        assert_send_mail_data(message_obj,
                              subject=CONFRIM_EMAIL_SUBJECT,
                              receiver=request_data['email'])

    def test_resend_with_invalid_callback_url_fails(self, client,
                                                    saved_valid_user_one,
                                                    valid_user_one_token):
        send_mail_as_html.delay = Mock(side_effect=send_mail_as_html)
        SendGridAPIClient.send = Mock(side_effect=lambda x: None)

        request_data = {
            'email': saved_valid_user_one.email,
            'callbackURL': 'ftp://abc',
        }
        response = client.post(
            RESEND_EMAIL_ENDPOINT,
            data=request_data,
            HTTP_AUTHORIZATION=f'Bearer {valid_user_one_token}')
        response_data = response.data

        assert response.status_code == 400
        assert response_data['message'] == error_messages.serialization_errors[
            'many_invalid_fields']
        assert response_data['errors']['callbackURL'] == \
               error_messages.serialization_errors['invalid_url_field']
        assert response_data['status'] == 'error'

    def test_resend_email_for_verified_user_fails(self, client,
                                                  saved_valid_user_one,
                                                  valid_user_one_token):
        """Should fail when the token is expired

        Args:
            client (fixture): a fixture used to make HTTP request
        """
        saved_valid_user_one.verified = True
        saved_valid_user_one.save()

        request_data = {
            'email': saved_valid_user_one.email,
            'callbackURL': 'https://test.com',
        }
        response = client.post(
            RESEND_EMAIL_ENDPOINT,
            data=request_data,
            HTTP_AUTHORIZATION=f'Bearer {valid_user_one_token}')

        response_data = response.data

        assert response.status_code == 400
        assert response_data['message'] == error_messages.serialization_errors[
            'user_already_verified']
        assert response_data['status'] == 'error'
