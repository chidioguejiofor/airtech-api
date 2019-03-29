from ..utils.success_messages import signup_route
from ..utils.error_messages import serialization_errors
from ..utils.constants import FIELD_IS_REQUIRED_STR
from .models import User
from django.db.utils import IntegrityError

import pytest


@pytest.mark.django_db
class TestUserModel:
    def test_save_user_to_db_succeeds(self, valid_user_one):
        model = User(**valid_user_one)
        model.save()
        assert valid_user_one['username'] == model.username
        assert valid_user_one['first_name'] == model.first_name
        assert valid_user_one['last_name'] == model.last_name
        assert valid_user_one['gender'] == model.gender
        assert valid_user_one['username'] == model.username

    def test_save_existing_user_fails(self, valid_user_two):
        model = User(**valid_user_two)
        model.save()  # saves the user to db
        model = User(**valid_user_two)

        with pytest.raises(IntegrityError):
            model.save()  # should fail here


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
        response = client.post(
            '/api/v1/signup', data=empty_dict, content_type="application/json")
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

        response = client.post(
            '/api/v1/signup',
            data=invalid_gender,
            content_type="application/json")
        response_body = response.data
        errors = response_body['errors']
        assert errors['gender'][0] == serialization_errors['invalid_gender']
        assert response.status_code == 400
        assert response_body['status'] == 'error'

    def test_signup_with_valid_data_succeeds(self, client):
        """Should return a welcome message to the user on GET /api


        Returns:
            None
        """

        valid_data = {
            "username": "age1201",
            "firstName": "MMM",
            "lastName": "fdajhfio",
            "email": "chid@email.com",
            "gender": "female",
            "password": "password"
        }
        # import pdb;
        # pdb.set_trace()
        response = client.post(
            '/api/v1/signup', data=valid_data, content_type="application/json")
        response_body = response.data
        data = response_body['data']

        assert response.status_code == 201
        assert response_body['status'] == 'success'
        assert response_body['message'] == signup_route['signup_success']
        assert 'id' in data
        assert 'createdAt' in data
        assert 'updatedAt' in data
        assert 'password' not in data
        assert data['gender'].lower() == 'female'
        assert data['firstName'] == valid_data['firstName']
        assert data['lastName'] == valid_data['lastName']
        assert data['email'] == valid_data['email']
