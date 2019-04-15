# Third Party Libraries
import pytest

from airtech_api.utils import success_messages
from airtech_api.utils.error_messages import serialization_errors
from airtech_api.utils.constants import FIELD_IS_REQUIRED_STR

from tests.mocks.users import valid_json_user


@pytest.mark.django_db
class TestSignupRoute:
    """
    Tests the /signup_route
    """

    def test_signup_with_data_is_missing_fails(self, client):
        """Should fail when an some or all fields are missing

        Args:
            client (fixture): a pytest fixture that is used to make HTTP Requests

        """
        empty_dict = {}
        response = client.post('/api/v1/signup',
                               data=empty_dict,
                               content_type="application/json")
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
        assert 'gender' in errors
        assert 'email' in errors
        assert 'username' in errors

        assert errors['gender'][0] == FIELD_IS_REQUIRED_STR
        assert errors['email'][0] == FIELD_IS_REQUIRED_STR
        assert errors['password'][0] == FIELD_IS_REQUIRED_STR
        assert errors['username'][0] == FIELD_IS_REQUIRED_STR

    def test_signup_with_invalid_gender_fails(self, client):
        """Should fail when the gender is invalid

        Returns:
            None
        """

        invalid_gender = {
            "username": "age1201",
            "firstName": "MMM",
            "lastName": "fdajhfio",
            "email": "chid@email.com",
            "gender": "invalid",
            "password": "password"
        }

        response = client.post('/api/v1/signup',
                               data=invalid_gender,
                               content_type="application/json")
        response_body = response.data
        errors = response_body['errors']
        assert errors['gender'][0] == serialization_errors['invalid_gender']
        assert response.status_code == 400
        assert response_body['status'] == 'error'

    def test_signup_with_gender_eq_male_succeeds(self, client):
        """Should return a welcome message to the user on GET /api


        Returns:
            None
        """
        json_user = dict(**valid_json_user)
        json_user['gender'] = 'male'
        response = client.post('/api/v1/signup',
                               data=json_user,
                               content_type="application/json")
        response_body = response.data
        data = response_body['data']

        assert response.status_code == 201
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages[
            'auth_successful'].format("Sign Up")
        assert 'id' in data
        assert 'token' in data
        assert 'password' not in data
        assert data['gender'].lower() == 'male'
        assert data['firstName'] == valid_json_user['firstName']
        assert data['lastName'] == valid_json_user['lastName']
        assert data['email'] == valid_json_user['email']

    def test_signup_with_gender_equals_female_succeeds(self, client):
        """Should return a welcome message to the user on GET /api


        Returns:
            None
        """
        json_user = dict(**valid_json_user)
        json_user['gender'] = 'female'

        response = client.post('/api/v1/signup',
                               data=json_user,
                               content_type="application/json")
        response_body = response.data
        data = response_body['data']

        assert response.status_code == 201
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages[
            'auth_successful'].format("Sign Up")
        assert 'id' in data
        assert 'token' in data
        assert 'password' not in data
        assert data['gender'].lower() == valid_json_user['gender']
        assert data['firstName'] == valid_json_user['firstName']
        assert data['lastName'] == valid_json_user['lastName']
        assert data['email'] == valid_json_user['email']
