import pytest

from airtech_api.utils import success_messages
from airtech_api.utils.error_messages import tokenization_errors, serialization_errors
from airtech_api.flight.models import Flight
from datetime import datetime, timedelta

from tests.mocks.flight import valid_flight_one
from tests.helpers.assertion_helpers import (
    assert_missing_header, assert_invalid_token_format, assert_forbidden_user,
    assert_token_is_invalid, assert_resource_not_found)


@pytest.mark.django_db
class TestFlightRoute:

    # POST
    def test_create_flight_with_valid_data_succeeds(
            self, client, valid_admin_user_token,
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
        assert float(
            response_data['currentPrice']) == valid_flight_one['currentPrice']
        assert response_data['type'] == valid_flight_one['type']
        assert response_data['updatedAt'] is None

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
        assert saved_valid_admin_user_model_one.admin is True

    def test_create_flight_with_schedule_less_than_now_fails(
            self, client, valid_admin_user_token,
            saved_valid_admin_user_model_one):

        invalid_schedule_dict = dict(**valid_flight_one)
        invalid_schedule_dict['schedule'] = datetime.now() - timedelta(days=1)
        response = client.post(
            '/api/v1/flight',
            data=invalid_schedule_dict,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )
        response_body = response.data

        assert response.status_code == 400
        assert response_body['status'] == 'error'

        assert response_body['message'] == serialization_errors[
            'many_invalid_fields']
        assert response_body['errors']['schedule'][0] == serialization_errors[
            'invalid_flight_schedule']

    def test_create_flight_with_invalid_flight_type_fails(
            self, client, valid_admin_user_token,
            saved_valid_admin_user_model_one):

        invalid_schedule_dict = dict(**valid_flight_one)
        invalid_schedule_dict['type'] = 'intercon'
        response = client.post(
            '/api/v1/flight',
            data=invalid_schedule_dict,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )
        response_body = response.data

        assert response.status_code == 400
        assert response_body['status'] == 'error'

        assert response_body['message'] == serialization_errors[
            'many_invalid_fields']
        assert response_body['errors']['type'][0] == serialization_errors[
            'invalid_flight_type']

    def test_create_flight_with_missing_header_fails(self, client):

        response = client.post(
            '/api/v1/flight',
            data=valid_flight_one,
            content_type='application/json')

        assert_missing_header(response)

    def test_create_flight_with_invalid_token_format_fails(
            self, client, valid_admin_user_token,
            saved_valid_admin_user_model_one):

        response = client.post(
            '/api/v1/flight',
            data=valid_flight_one,
            content_type='application/json',
            HTTP_AUTHORIZATION='{}'.format(valid_admin_user_token),
        )

        assert_invalid_token_format(response)

    def test_non_admin_user_creates_flight_fails(self, client,
                                                 valid_user_one_token):

        response = client.post(
            '/api/v1/flight',
            data=valid_flight_one,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        assert_forbidden_user(response)

    # GET ALL
    def test_get_all_flights_with_valid_token_succeeds(self, client,
                                                       valid_user_one_token):

        response = client.get(
            '/api/v1/flight',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_body = response.data
        response_data = response_body['data']
        meta = response_body['meta']
        assert response.status_code == 200
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages[
            'retrieved'].format('Flights')
        assert isinstance(response_data, list)
        assert isinstance(response_body['meta'], dict)
        assert meta['currentPage'] == 1
        assert meta['previousPageNumber'] is None
        assert meta['itemsPerPage'] == 10

    def test_get_all_flights_with_pagination_query_succeeds(
            self, client, valid_user_one_token, saved_bulk_inserted_flights):

        response = client.get(
            '/api/v1/flight?page=2&limit=5',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_body = response.data
        response_data = response_body['data']
        meta = response_body['meta']
        assert response.status_code == 200
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages[
            'retrieved'].format('Flights')
        assert isinstance(response_data, list)
        assert isinstance(response_body['meta'], dict)
        assert meta['currentPage'] == 2
        assert meta['previousPageNumber'] == 1
        assert meta['nextPageNumber'] == 3
        assert meta['itemsPerPage'] == 5

    def test_get_all_flights_with_valid_admin_token_succeeds(
            self, client, valid_admin_user_token):

        response = client.get(
            '/api/v1/flight',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )

        response_body = response.data
        response_data = response_body['data']
        meta = response_body['meta']
        assert response.status_code == 200
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages[
            'retrieved'].format('Flights')
        assert isinstance(response_data, list)
        assert isinstance(response_body['meta'], dict)
        assert meta['currentPage'] == 1
        assert meta['previousPageNumber'] is None
        assert meta['itemsPerPage'] == 10

    def test_get_all_with_invalid_token_fails(self, client):
        response = client.get(
            '/api/v1/flight',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format('invalid-token'),
        )

        assert_token_is_invalid(response)

    # GET One
    def test_get_specific_flight_with_valid_id_succeeds(
            self, client, saved_valid_admin_user_model_one,
            valid_user_one_token):
        model = Flight(
            **valid_flight_one, created_by=saved_valid_admin_user_model_one)
        model.save()

        response = client.get(
            '/api/v1/flight/{}'.format(model.id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_body = response.data
        data = response_body['data']
        assert response.status_code == 200
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages[
            'retrieved'].format('Flight')
        assert data['id'] == str(model.id)

    def test_get_with_invalid_uuid_format_fails(
            self, client, saved_valid_admin_user_model_one,
            valid_user_one_token):

        invalid_uuid = 'invalid-uuid'
        response = client.get(
            '/api/v1/flight/{}'.format(invalid_uuid),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        assert_resource_not_found(response, 'Flight', invalid_uuid)

    def test_get_specific_flight_with_invalid_token_fails(
            self, client, saved_valid_admin_user_model_one):
        model = Flight(
            **valid_flight_one, created_by=saved_valid_admin_user_model_one)
        model.save()

        response = client.get(
            '/api/v1/flight/{}'.format(model.id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format('invalid-token'),
        )
        assert_token_is_invalid(response)
