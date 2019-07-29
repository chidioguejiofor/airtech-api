# Third Party Libraries
import pytest
from airtech_api.users.models import User
from airtech_api.utils.error_messages import serialization_errors, tokenization_errors
from airtech_api.utils import success_messages
from airtech_api.utils.constants import ADMIN_REQUEST_SUBJECT
from tests.helpers.assertion_helpers import assert_redirect_response
from airtech_api.utils.constants import TEST_HOST_NAME
from airtech_api.services.email_service.send_mail import send_mail_as_html
from unittest.mock import Mock
from sendgrid import SendGridAPIClient

from tests.helpers.assertion_helpers import assert_send_mail_data
CONFIRM_ADMIN_REQUEST_ENDPOINT = '/api/v1/auth/request-admin-access/{}'
ADMIN_REQUEST_ENDPOINT = '/api/v1/auth/request-admin-access'


@pytest.mark.django_db
class TestConfirmAdminRequestEndpoint:
    """
    Tests the confirm email route
    """

    def test_confirm_with_invalid_token_fails(self, client,
                                              saved_valid_user_one,
                                              invalid_confirm_account_token):
        """Should fail when the token is invalid

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one (model): a model that represents a user in the db
        """

        response = client.get(
            CONFIRM_ADMIN_REQUEST_ENDPOINT.format(
                invalid_confirm_account_token))
        user = User.objects.get(pk=saved_valid_user_one.pk)
        assert_redirect_response(response, 'false')
        assert user.admin is False

    def test_confirm_with_expired_token_fails(
            self, client, expired_user_one_confirm_account_token,
            saved_valid_user_one):
        """Should fail when the token is expired

        Args:
            client (fixture): a fixture used to make HTTP request
            expired_user_one_confirm_account_token (str): the expired user one token
            saved_valid_user_one(model): a model that represents a user in the db
        """

        response = client.get(
            CONFIRM_ADMIN_REQUEST_ENDPOINT.format(
                expired_user_one_confirm_account_token))
        assert_redirect_response(response, 'false')
        user = User.objects.get(pk=saved_valid_user_one.pk)
        assert user.verified is False

    def test_confirm_with_a_token_of_non_existing_user_fails(
            self, client, non_existing_user_confirm_account_token,
            saved_valid_user_one):
        """Should fail when the token is expired

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one(model): a model that represents a user in the db
        """

        response = client.get(
            CONFIRM_ADMIN_REQUEST_ENDPOINT.format(
                non_existing_user_confirm_account_token))
        user = User.objects.get(pk=saved_valid_user_one.pk)
        assert response.status_code == 302
        assert user.admin is False

    def test_confirm_admin_request_succeeds(self, client,
                                            valid_admin_request_token,
                                            saved_valid_user_one):
        """Should succeed when a valid token is used

           Args:
               client (fixture): a fixture used to make HTTP request
               valid_user_one_confirm_account_token (str): the user one valid token
               saved_valid_user_one(model): a model that represents a user in the db
        """
        saved_valid_user_one.verified = True
        saved_valid_user_one.admin = False
        saved_valid_user_one.save()
        response = client.get(
            CONFIRM_ADMIN_REQUEST_ENDPOINT.format(valid_admin_request_token))
        user = User.objects.get(pk=saved_valid_user_one.pk)
        assert response.status_code == 302
        assert response.url.startswith(f'http://{TEST_HOST_NAME}/login')
        assert user.admin is True


@pytest.mark.django_db
class TestMakeAdminRequestEndpoint:
    """
    Tests the confirm email route
    """

    def test_make_admin_request_for_unverified_user_fails(
            self, client, saved_valid_user_one, valid_user_one_token):
        """Should fail when the user is unverified

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one (model): a model that represents a user in the db
        """
        saved_valid_user_one.verified = False
        saved_valid_user_one.image_url = 'http://temp.com/here'
        saved_valid_user_one.admin = False
        saved_valid_user_one.save()
        request_data = {
            'callbackURL': 'http://test.com',
        }

        response = client.post(
            ADMIN_REQUEST_ENDPOINT,
            data=request_data,
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        user = User.objects.get(pk=saved_valid_user_one.pk)

        assert response.status_code == 403
        assert response.data['message'] == tokenization_errors[
            'unverified_account']
        assert user.admin is False

    def test_make_admin_request_with_missing_callback_url_fails(
            self, client, saved_valid_user_one, valid_user_one_token):
        """Should fail when the user is unverified

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one (model): a model that represents a user in the db
        """
        saved_valid_user_one.verified = True
        saved_valid_user_one.image_url = 'http://temp.com/here'
        saved_valid_user_one.admin = False
        saved_valid_user_one.save()
        response = client.post(
            ADMIN_REQUEST_ENDPOINT,
            data={},
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        user = User.objects.get(pk=saved_valid_user_one.pk)

        errors = response.data['errors']
        assert response.status_code == 400
        assert errors['callbackURL'][0] == serialization_errors[
            'invalid_url_field']
        assert response.data['message'] == serialization_errors[
            'many_invalid_fields']
        assert user.admin is False

    def test_make_admin_request_for_user_without_profile_fails(
            self, client, saved_valid_user_one, valid_user_one_token):
        """Should fail when the user has not updated his profile

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one (model): a model that represents a user in the db
        """
        saved_valid_user_one.verified = True
        saved_valid_user_one.image_url = None
        saved_valid_user_one.admin = False
        saved_valid_user_one.save()
        request_data = {
            'callbackURL': 'http://test.com',
        }

        response = client.post(
            ADMIN_REQUEST_ENDPOINT,
            data=request_data,
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        user = User.objects.get(pk=saved_valid_user_one.pk)
        assert response.status_code == 403
        assert response.data['message'] == serialization_errors[
            'profile_not_updated']
        assert user.admin is False

    def test_make_admin_request_when_user_inputs_valid_data_succeeds(
            self, client, saved_valid_user_one, valid_user_one_token):
        """Should succeed valid user inputs all required data

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one (model): a model that represents a user in the db
        """
        import os
        send_mail_as_html.delay = Mock(side_effect=send_mail_as_html)
        SendGridAPIClient.send = Mock(side_effect=lambda x: None)
        saved_valid_user_one.verified = True
        saved_valid_user_one.image_url = 'http://test.com'
        saved_valid_user_one.admin = False
        saved_valid_user_one.save()
        request_data = {
            'callbackURL': 'http://test.com',
        }

        response = client.post(
            ADMIN_REQUEST_ENDPOINT,
            data=request_data,
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        user = User.objects.get(pk=saved_valid_user_one.pk)
        assert response.status_code == 200
        assert response.data['message'] == success_messages[
            'admin_request_sent']
        assert response.data['status'] == 'success'
        assert user.admin is False
        message_obj = SendGridAPIClient.send.call_args[0][0]
        assert_send_mail_data(message_obj,
                              subject=ADMIN_REQUEST_SUBJECT,
                              receiver=os.getenv('OWNER_EMAIL'))

    def test_admin_user_makes_admin_request_fails(
            self, client, saved_valid_admin_user_model_one,
            valid_admin_user_token):
        """Should fail when the usetest_resend_with_invalid_callback_url_failsr has not updated his profile

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one (model): a model that represents a user in the db
        """
        saved_valid_admin_user_model_one.verified = True
        saved_valid_admin_user_model_one.image_url = 'http://here.com'
        saved_valid_admin_user_model_one.save()
        request_data = {
            'callbackURL': 'http://test.com',
        }

        response = client.post(
            ADMIN_REQUEST_ENDPOINT,
            data=request_data,
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )
        user = User.objects.get(pk=saved_valid_admin_user_model_one.pk)
        assert response.status_code == 403
        assert response.data['message'] == serialization_errors[
            'regular_user_only']
        assert user.admin
