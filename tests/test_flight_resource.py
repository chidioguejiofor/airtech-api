import pytest
from airtech_api.booking.models import Booking
from airtech_api.utils import success_messages
from airtech_api.utils.error_messages import serialization_errors
from airtech_api.flight.models import Flight
from datetime import datetime, timedelta

from tests.mocks.flight import valid_flight_one, camelized_valid_flight_one
from tests.helpers.assertion_helpers import (assert_missing_header,
                                             assert_invalid_token_format,
                                             assert_forbidden_user,
                                             assert_token_is_invalid,
                                             assert_resource_not_found)

FLIGHT_URL = '/api/v1/flights'
SINGLE_FLIGHT_URL = '/api/v1/flights/{}'


@pytest.mark.django_db
class TestFlightRoute:

    # POST
    def test_create_flight_with_valid_data_succeeds(
            self, client, valid_admin_user_token,
            saved_valid_admin_user_model_one):

        response = client.post(
            FLIGHT_URL,
            data=camelized_valid_flight_one,
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
        assert 'id' in response_data
        assert 'updatedAt' in response_data
        assert 'createdAt' in response_data

        # Assert Flight values
        assert response_data['capacity'] == valid_flight_one['capacity']
        assert response_data['location'] == valid_flight_one['location']
        assert response_data['destination'] == valid_flight_one['destination']
        assert float(
            response_data['currentPrice']) == valid_flight_one['current_price']
        assert response_data['type'] == valid_flight_one['type']
        assert response_data['updatedAt'] is None

        creator_model = Flight.objects.get(pk=response_data['id']).created_by

        # Assert Creator values
        assert creator_model.id == saved_valid_admin_user_model_one.id
        assert creator_model.first_name == saved_valid_admin_user_model_one.first_name
        assert creator_model.last_name == saved_valid_admin_user_model_one.last_name
        assert creator_model.gender == saved_valid_admin_user_model_one.gender

        # Assert that the user is admin
        assert saved_valid_admin_user_model_one.admin is True

    def test_create_flight_with_schedule_less_than_now_fails(
            self, client, valid_admin_user_token,
            saved_valid_admin_user_model_one):

        invalid_schedule_dict = dict(**valid_flight_one)
        invalid_schedule_dict['schedule'] = datetime.now() - timedelta(days=1)
        response = client.post(
            FLIGHT_URL,
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
            FLIGHT_URL,
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

        response = client.post(FLIGHT_URL,
                               data=valid_flight_one,
                               content_type='application/json')

        assert_missing_header(response)

    def test_create_flight_with_invalid_token_format_fails(
            self, client, valid_admin_user_token,
            saved_valid_admin_user_model_one):

        response = client.post(
            FLIGHT_URL,
            data=valid_flight_one,
            content_type='application/json',
            HTTP_AUTHORIZATION='{}'.format(valid_admin_user_token),
        )

        assert_invalid_token_format(response)

    def test_non_admin_user_creates_flight_fails(self, client,
                                                 valid_user_one_token):

        response = client.post(
            FLIGHT_URL,
            data=valid_flight_one,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        assert_forbidden_user(response)

    # GET ALL
    def test_get_all_flights_with_valid_token_succeeds(self, client,
                                                       valid_user_one_token):

        response = client.get(
            FLIGHT_URL,
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
            FLIGHT_URL + '?page=2&limit=5',
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
            FLIGHT_URL,
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
            FLIGHT_URL,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format('invalid-token'),
        )

        assert_token_is_invalid(response)

    # GET One
    def test_get_specific_flight_with_valid_id_succeeds(
            self, client, saved_valid_admin_user_model_one,
            valid_user_one_token):
        model = Flight(**valid_flight_one,
                       created_by=saved_valid_admin_user_model_one)
        model.save()

        response = client.get(
            SINGLE_FLIGHT_URL.format(model.id),
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
            SINGLE_FLIGHT_URL.format(invalid_uuid),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        assert_resource_not_found(response, 'Flight', invalid_uuid)

    def test_get_specific_flight_with_invalid_token_fails(
            self, client, saved_valid_admin_user_model_one):
        model = Flight(**valid_flight_one,
                       created_by=saved_valid_admin_user_model_one)
        model.save()

        response = client.get(
            SINGLE_FLIGHT_URL.format(model.id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format('invalid-token'),
        )
        assert_token_is_invalid(response)

    # UPDATE ROUTE
    def test_update_flight_with_correct_data_succeeds(
            self, client, valid_admin_user_token,
            saved_valid_flight_model_two):
        update_data = {
            'capacity': 100000,
            'type': 'international',
            'currentPrice': 500_000
        }
        old_updated_at = saved_valid_flight_model_two.updated_at

        response = client.patch(
            SINGLE_FLIGHT_URL.format(saved_valid_flight_model_two.id),
            content_type='application/json',
            data=update_data,
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )

        assert response.status_code == 201
        res_body = response.data['data']

        assert res_body['capacity'] == update_data['capacity']
        assert res_body['type'] == update_data['type']
        assert res_body['currentPrice'] == update_data['currentPrice']
        assert old_updated_at != res_body['updatedAt']

    def test_update_flight_with_invalid_values_fails(
            self, client, valid_admin_user_token,
            saved_valid_flight_model_two):
        update_data = {
            'capacity': 'not a number',
            'type': 'abracada',
            'currentPrice': 'certainly invalid',
        }

        response = client.patch(
            SINGLE_FLIGHT_URL.format(saved_valid_flight_model_two.id),
            content_type='application/json',
            data=update_data,
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )

        res_body = response.data
        flight = Flight.objects.get(pk=saved_valid_flight_model_two.id)

        assert response.status_code == 400

        assert res_body['status'] == 'error'
        assert res_body['message'] == serialization_errors[
            'many_invalid_fields']
        assert res_body['errors']['type'][0] == serialization_errors[
            'invalid_flight_type']
        assert res_body['errors']['capacity'][
            0] == 'A valid integer is required.'
        assert res_body['errors']['currentPrice'][
            0] == 'A valid integer is required.'

        assert str(flight.capacity) != update_data['capacity']
        assert str(flight.current_price) != update_data['currentPrice']
        assert flight.type != update_data['type']

    def test_update_flight_no_request_body_fails(self, client,
                                                 valid_admin_user_token,
                                                 saved_valid_flight_model_two):

        response = client.patch(
            SINGLE_FLIGHT_URL.format(saved_valid_flight_model_two.id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )

        res_body = response.data

        assert response.status_code == 400
        assert res_body['status'] == 'error'
        assert res_body['message'] == serialization_errors[
            'empty_request'].format('Flight')

    def test_attempt_to_update_location_when_bookings_have_been_made_fails(
            self, client, valid_admin_user_token, saved_valid_flight_model_two,
            saved_valid_user_one):
        update_data = {
            'location': 'Abuja, Lagos',
        }
        Booking.objects.create(
            flight_model=saved_valid_flight_model_two,
            ticket_price=saved_valid_flight_model_two.current_price,
            created_by=saved_valid_user_one,
        )
        response = client.patch(
            SINGLE_FLIGHT_URL.format(saved_valid_flight_model_two.id),
            content_type='application/json',
            data=update_data,
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )

        res_body = response.data
        flight = Flight.objects.get(pk=saved_valid_flight_model_two.id)

        assert response.status_code == 400

        assert res_body['status'] == 'error'
        assert res_body['message'] == serialization_errors[
            'many_invalid_fields']
        assert res_body['errors']['location'][0] == \
               serialization_errors['cannot_update_flight_field_with_bookings'].format('location')

        assert str(flight.location) != update_data['location']

    def test_attempt_to_update_destination_when_bookings_have_been_made_fails(
            self, client, valid_admin_user_token, saved_valid_flight_model_two,
            saved_valid_user_one):
        update_data = {
            'destination': 'Aba Kingdom',
        }
        Booking.objects.create(
            flight_model=saved_valid_flight_model_two,
            ticket_price=saved_valid_flight_model_two.current_price,
            created_by=saved_valid_user_one,
        )
        response = client.patch(
            SINGLE_FLIGHT_URL.format(saved_valid_flight_model_two.id),
            content_type='application/json',
            data=update_data,
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )

        res_body = response.data
        flight = Flight.objects.get(pk=saved_valid_flight_model_two.id)

        assert response.status_code == 400

        assert res_body['status'] == 'error'
        assert res_body['message'] == serialization_errors[
            'many_invalid_fields']
        assert res_body['errors']['destination'][0] == \
               serialization_errors['cannot_update_flight_field_with_bookings'].format('destination')

        assert str(flight.destination) != update_data['destination']

    def test_attempt_to_update_schedule_fails(self, client,
                                              valid_admin_user_token,
                                              saved_valid_flight_model_two,
                                              saved_valid_user_one):
        update_data = {
            'schedule': str(datetime.now()),
        }
        response = client.patch(
            SINGLE_FLIGHT_URL.format(saved_valid_flight_model_two.id),
            content_type='application/json',
            data=update_data,
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )

        res_body = response.data
        flight = Flight.objects.get(pk=saved_valid_flight_model_two.id)

        assert response.status_code == 400

        assert res_body['status'] == 'error'
        assert res_body['message'] == serialization_errors[
            'many_invalid_fields']
        assert res_body['errors']['schedule'][0] == \
               serialization_errors['cannot_update_field'].format('Flight', 'schedule')

        assert str(flight.schedule) != update_data['schedule']

    #  DELETE
    def test_delete_flight_with_no_booking_succeeds(
            self, client, saved_valid_admin_user_model_one,
            saved_valid_flight_model_two, valid_admin_user_token):
        response = client.delete(
            SINGLE_FLIGHT_URL.format(saved_valid_flight_model_two.id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )
        body = response.data
        assert response.status_code == 200
        assert body['status'] == 'success'
        assert body['message'] == success_messages['deleted'].format(
            'Flight', saved_valid_flight_model_two.id)
        assert len(
            Flight.objects.filter(id=saved_valid_flight_model_two.id)) == 0

    def test_delete_flight_with_booking_fails(self, client,
                                              saved_valid_user_one,
                                              saved_valid_flight_model_two,
                                              valid_admin_user_token):
        Booking.objects.create(
            flight_model=saved_valid_flight_model_two,
            ticket_price=saved_valid_flight_model_two.current_price,
            created_by=saved_valid_user_one,
        )
        response = client.delete(
            SINGLE_FLIGHT_URL.format(saved_valid_flight_model_two.id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )

        res_body = response.data

        assert response.status_code == 400
        assert res_body['status'] == 'error'
        assert res_body['message'] == serialization_errors[
            'cannot_delete_flight_with_bookings']
        assert Flight.objects.get(pk=saved_valid_flight_model_two.id)

    def test_delete_flight_with_expired_schedule_fails(
            self, client, saved_valid_user_one, saved_valid_flight_model_two,
            valid_admin_user_token):
        saved_valid_flight_model_two.schedule = datetime.now() - timedelta(
            minutes=1)
        saved_valid_flight_model_two.save()
        response = client.delete(
            SINGLE_FLIGHT_URL.format(saved_valid_flight_model_two.id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )

        res_body = response.data

        assert response.status_code == 400
        assert res_body['status'] == 'error'
        assert res_body['message'] == serialization_errors[
            'cannot_delete_flight_that_has_flown']
        assert Flight.objects.get(pk=saved_valid_flight_model_two.id)
