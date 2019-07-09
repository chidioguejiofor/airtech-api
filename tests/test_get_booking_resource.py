import pytest

from airtech_api.utils import success_messages
from airtech_api.booking.models import Booking
from airtech_api.utils.error_messages import serialization_errors
from airtech_api.flight.models import Flight
from datetime import datetime, timedelta
from django.utils import timezone
from tests.helpers.assertion_helpers import (assert_missing_header,
                                             assert_invalid_token_format,
                                             assert_forbidden_user,
                                             assert_token_is_invalid,
                                             assert_resource_not_found)
from uuid import uuid4

USER_BOOKING_URL = '/api/v1/user/bookings'


@pytest.mark.django_db
class TestUserBookingRoute:

    # GET ALL
    def test_get_all_bookings_with_valid_token_succeeds(
            self, client, valid_user_one_token,
            saved_bulk_inserted_bookings_for_user_one):

        response = client.get(
            USER_BOOKING_URL,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_body = response.data
        response_data = response_body['data']
        meta = response_body['meta']
        assert response.status_code == 200
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages[
            'retrieved'].format('Bookings')
        assert isinstance(response_data, list)
        assert isinstance(response_body['meta'], dict)
        assert meta['currentPage'] == 1
        assert meta['previousPageNumber'] is None
        assert meta['itemsPerPage'] == 10

    def test_get_all_bookings_with_pagination_query_succeeds(
            self, client, valid_user_one_token,
            saved_bulk_inserted_bookings_for_user_one):

        response = client.get(
            USER_BOOKING_URL + '?page=2&limit=5',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_body = response.data
        response_data = response_body['data']
        meta = response_body['meta']
        assert response.status_code == 200
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages[
            'retrieved'].format('Bookings')
        assert isinstance(response_data, list)
        assert isinstance(response_body['meta'], dict)
        assert meta['currentPage'] == 2
        assert meta['previousPageNumber'] == 1
        assert meta['nextPageNumber'] == 3
        assert meta['itemsPerPage'] == 5

    def test_get_bookings_with_valid_admin_token_succeeds(
            self, client, valid_admin_user_token):

        response = client.get(
            USER_BOOKING_URL,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_admin_user_token),
        )

        response_body = response.data
        response_data = response_body['data']
        meta = response_body['meta']
        assert response.status_code == 200
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages[
            'retrieved'].format('Bookings')
        assert isinstance(response_data, list)
        assert isinstance(response_body['meta'], dict)
        assert meta['currentPage'] == 1
        assert meta['previousPageNumber'] is None
        assert meta['itemsPerPage'] == 10

    def test_get_all_bookings_with_invalid_token_fails(self, client):
        response = client.get(
            USER_BOOKING_URL,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format('invalid-token'),
        )

        assert_token_is_invalid(response)

    def test_get_all_bookings_with_missing_id_fails(self, client):
        response = client.get(
            USER_BOOKING_URL,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(uuid4()),
        )
        assert_token_is_invalid(response)

    def test_delete_bookings_succeeds(self, client, saved_valid_booking, valid_user_one_token):
        response = client.delete(
            USER_BOOKING_URL + f'/{saved_valid_booking.pk}',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        response_body = response.data
        assert response.status_code == 200
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages[
            'deleted'].format('Booking', saved_valid_booking.id)

    def test_delete_expired_booking_fails(self, client, expired_booking, valid_user_one_token):
        response = client.delete(
            USER_BOOKING_URL + f'/{expired_booking.pk}',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        response_body = response.data
        assert response.status_code == 400
        assert response_body['status'] == 'error'
        assert response_body['message'] == serialization_errors[
            'cannot_delete_expired_booking']

    def test_user_attempt_to_delete_booking_that_is_not_his_fails(self, client, saved_valid_booking, valid_user_two_token):
        response = client.delete(
            USER_BOOKING_URL + f'/{saved_valid_booking.pk}',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_two_token),
        )
        response_body = response.data
        assert response.status_code == 404
        assert response_body['status'] == 'error'
        assert response_body['message'] == serialization_errors[
            'resource_id_not_found'].format('Booking')

    def test_delete_booking_that_has_been_paid_for_fails(self, client, saved_valid_booking, valid_user_one_token):
        saved_valid_booking.paid_at = timezone.now()
        saved_valid_booking.save()

        response = client.delete(
            USER_BOOKING_URL + f'/{saved_valid_booking.pk}',
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        response_body = response.data
        assert response.status_code == 400
        assert response_body['status'] == 'error'
        assert response_body['message'] == serialization_errors[
            'paid_booking_cannot_be_deleted']



@pytest.mark.django_db
class TestBookingModel:
    def test_cannot_save_booking_with_no_expiry_date(
            self, saved_bulk_inserted_bookings_for_user_one):
        booking_one = saved_bulk_inserted_bookings_for_user_one[0]
        booking_one.expiry_date = None
        with pytest.raises(Exception):
            assert booking_one.save()
