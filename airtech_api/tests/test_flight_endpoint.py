import pytest

from airtech_api.utils import success_messages
from airtech_api.utils.error_messages import tokenization_errors


@pytest.mark.django_db
class TestFlightRoute:
    def test_create_flight_with_valid_data_succeeds(
            self, client, valid_flight_one, valid_admin_user_token,
            saved_valid_admin_user_model_one):

        response = client.post(
            '/api/v1/flight',
            data=valid_flight_one,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )

        response_body = response.data
        response_data = response.data['data']

        assert response.status_code == 201

        # Assert Response Body values
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages[
            'resource_created'].format('Flight')

        # Fields that should be in the Response Body
        assert 'creator' in response_data
        assert 'id' in response_data
        assert 'updatedAt' in response_data
        assert 'createdAt' in response_data

        # Assert Flight values
        assert response_data['capacity'] == valid_flight_one['capacity']
        assert response_data['location'] == valid_flight_one['location']
        assert response_data['destination'] == valid_flight_one['destination']
        assert float(response_data['amount']) == valid_flight_one['amount']
        assert response_data['type'] == valid_flight_one['type']
        assert response_data['updatedAt'] == None

        # Assert Creator values
        assert response_data['creator']['id'] == str(
            saved_valid_admin_user_model_one.id)
        assert response_data['creator'][
            'firstName'] == saved_valid_admin_user_model_one.first_name
        assert response_data['creator'][
            'lastName'] == saved_valid_admin_user_model_one.last_name
        assert response_data['creator'][
            'gender'] == saved_valid_admin_user_model_one.gender

        # Assert that the user is admin
        saved_valid_admin_user_model_one.admin == True

    def test_create_flight_with_missing_header_fails(self, client,
                                                     valid_flight_one):

        response = client.post(
            '/api/v1/flight',
            data=valid_flight_one,
            content_type='application/json')

        response_body = response.data

        assert response.status_code == 401  # unauthorized
        assert response_body['status'] == 'error'
        assert response_body['message'] == tokenization_errors['missing_token']

    def test_create_flight_with_invalid_token_format_fails(
            self, client, valid_flight_one, valid_admin_user_token,
            saved_valid_admin_user_model_one):

        response = client.post(
            '/api/v1/flight',
            data=valid_flight_one,
            content_type='application/json',
            HTTP_AUTHORIZATION='{}'.format(valid_admin_user_token),
        )

        response_body = response.data

        assert response.status_code == 401  # unauthorized
        assert response_body['status'] == 'error'
        assert response_body['message'] == tokenization_errors[
            'token_format_error']

    def test_non_admin_user_creates_flight_fails(
            self, client, valid_flight_one, valid_user_one_token):

        response = client.post(
            '/api/v1/flight',
            data=valid_flight_one,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_body = response.data

        assert response.status_code == 403  # forbidden
        assert response_body['status'] == 'error'
        assert response_body['message'] == tokenization_errors[
            'user_is_forbidden']
