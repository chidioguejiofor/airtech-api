# Third Party Libraries
import pytest

from airtech_api.utils import success_messages
from airtech_api.users.models import User
from airtech_api.utils.error_messages import serialization_errors
from airtech_api.utils.constants import FIELD_IS_REQUIRED_STR


@pytest.mark.django_db
class TestLoginRoute:
    """
    Tests the /signup_route
    """

    def test_login_with_data_is_missing_fails(self, client):
        """Should fail when an some or all fields are missing

        Args:
            client (fixture): a pytest fixture that is used to make HTTP Requests

        """
        empty_dict = {}
        response = client.post(
            '/api/v1/login', data=empty_dict, content_type="application/json")
        response_body = response.data
        errors = response_body['errors']

        assert response.status_code == 400
        assert response_body['status'] == 'error'
        assert response_body['message'] == serialization_errors[
            'many_invalid_fields']

        assert 'id' not in errors
        assert 'createdAt' not in errors
        assert 'updatedAt' not in errors

        assert 'password' in errors
        assert 'usernameOrEmail' in errors

        assert errors['usernameOrEmail'][0] == FIELD_IS_REQUIRED_STR
        assert errors['password'][0] == FIELD_IS_REQUIRED_STR

    def test_login_with_valid_data_succeeds(self, client, valid_user_three):
        """Should succeed when the valid credentials are passed

        Returns:
            None
        """
        model = User(**valid_user_three)
        model.save()

        valid_data = {
            'usernameOrEmail': valid_user_three['username'],
            'password': valid_user_three['password'],
        }

        response = client.post(
            '/api/v1/login', data=valid_data, content_type="application/json")
        response_body = response.data
        data = response_body['data']
        assert response.status_code == 200
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages[
            'auth_successful'].format("Login")
        assert 'id' in data
        assert 'createdAt' in data
        assert 'updatedAt' in data
        assert 'token' in data
        assert 'password' not in data
        assert data['gender'].lower() == valid_user_three['gender']
        assert data['username'] == valid_user_three['username']
        assert data['firstName'] == valid_user_three['first_name']
        assert data['lastName'] == valid_user_three['last_name']
        assert data['email'] == valid_user_three['email']

    def test_login_when_user_is_not_found_fails(self, client):
        """Should fail when the user is not found

        Returns:
            None
        """

        user_not_in_db_data = {
            'usernameOrEmail': 'unknown101',
            'password': 'password',
        }

        response = client.post(
            '/api/v1/login',
            data=user_not_in_db_data,
            content_type="application/json")
        response_body = response.data
        assert response.status_code == 404
        assert response_body['status'] == 'error'
        assert response_body['message'] == serialization_errors[
            'user_not_found']
