# Third Party Libraries
import pytest
from airtech_api.users.models import User

from tests.helpers.assertion_helpers import assert_redirect_response, assert_expired_token
from airtech_api.utils.constants import TEST_HOST_NAME
CONFIRM_EMAIL_ENDPOINT = '/api/v1/auth/confirm-email/{}'


@pytest.mark.django_db
class TestConfirmEmailEndpoint:
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
            CONFIRM_EMAIL_ENDPOINT.format(invalid_confirm_account_token))
        user = User.objects.get(pk=saved_valid_user_one.pk)
        assert_redirect_response(response, 'false')
        assert user.verified is False

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
            CONFIRM_EMAIL_ENDPOINT.format(
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
            CONFIRM_EMAIL_ENDPOINT.format(
                non_existing_user_confirm_account_token))
        user = User.objects.get(pk=saved_valid_user_one.pk)
        assert response.status_code == 302
        assert user.verified is False

    def test_confirm_email_succeeds(self, client,
                                    valid_user_one_confirm_account_token,
                                    saved_valid_user_one):
        """Should succeed when a valid token is used

           Args:
               client (fixture): a fixture used to make HTTP request
               valid_user_one_confirm_account_token (str): the user one valid token
               saved_valid_user_one(model): a model that represents a user in the db
        """

        response = client.get(
            CONFIRM_EMAIL_ENDPOINT.format(
                valid_user_one_confirm_account_token))
        user = User.objects.get(pk=saved_valid_user_one.pk)
        assert response.status_code == 302
        assert response.url.startswith(f'http://{TEST_HOST_NAME}/login')
        assert user.verified is True
