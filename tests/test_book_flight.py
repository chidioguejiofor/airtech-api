import pytest
from datetime import datetime, timedelta
from airtech_api.utils import success_messages
from airtech_api.utils.error_messages import serialization_errors
from tests.helpers.assertion_helpers import (
    assert_token_is_invalid, assert_invalid_token_format, assert_expired_token,
    assert_resource_not_found)

from uuid import uuid4
from dateutil.parser import parse


@pytest.mark.django_db
class TestFlightRoute:

    # POST
    def test_book_flight_succeeds(self, client, valid_user_one_token,
                                  saved_valid_user_one,
                                  saved_valid_flight_model_one):
        valid_flight_id = str(saved_valid_flight_model_one.id)
        response = client.post(
            '/api/v1/flight/{}/booking'.format(valid_flight_id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        response_body = response.data
        response_data = response.data['data']
        assert response.status_code == 201
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages['booking_success']

        assert float(response_data['ticketPrice']
                     ) == saved_valid_flight_model_one.currentPrice
        assert response_data['flight']['id'] == str(
            saved_valid_flight_model_one.id)
        assert response_data['bookedBy']['id'] == str(saved_valid_user_one.id)

        assert 'createdAt' in response_data
        assert 'creator' not in response_data['flight']
        #

    def test_book_flight_with_days_to_flight_gte_60_succeeds(
            self, client, saved_flight_with_days_to_flight_gt_60,
            saved_valid_user_one, valid_user_one_token):
        """Should book flight when the days to flight is gte 60

        The expiryDate in this case should be set to 20 days before the flight

        Returns:
            None
        """
        valid_flight_id = str(saved_flight_with_days_to_flight_gt_60.id)
        response = client.post(
            '/api/v1/flight/{}/booking'.format(valid_flight_id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_body = response.data
        response_data = response.data['data']
        exp_time = parse(response_data['expiryDate'])
        schedule = saved_flight_with_days_to_flight_gt_60.schedule
        time_diff = schedule - exp_time

        assert response.status_code == 201
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages['booking_success']
        assert time_diff == timedelta(days=20)

    def test_book_flight_with_days_to_flight_btw_30_and_59_succeeds(
            self, client, saved_flight_with_days_to_flight_btw_30_and_59,
            saved_valid_user_one, valid_user_one_token):
        """Should book flight when the days to flight is btw 30 and 59

        The expiryDate in this case should be set to 5 days before the flight

        Returns:
            None
        """
        valid_flight_id = str(
            saved_flight_with_days_to_flight_btw_30_and_59.id)
        response = client.post(
            '/api/v1/flight/{}/booking'.format(valid_flight_id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_body = response.data
        response_data = response.data['data']
        exp_time = parse(response_data['expiryDate'])
        schedule = saved_flight_with_days_to_flight_btw_30_and_59.schedule
        time_diff = schedule - exp_time

        assert response.status_code == 201
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages['booking_success']
        assert time_diff == timedelta(days=5)

    def test_book_flight_with_days_to_flight_btw_7_and_29_succeeds(
            self, client, saved_flight_with_days_to_flight_btw_7_and_29,
            saved_valid_user_one, valid_user_one_token):
        """Should book flight when the days to flight ibtw 29 and 7

        The expiryDate in this case should be set to 24 hours before the flight

        Returns:
            None
        """
        valid_flight_id = str(saved_flight_with_days_to_flight_btw_7_and_29.id)
        response = client.post(
            '/api/v1/flight/{}/booking'.format(valid_flight_id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_body = response.data
        response_data = response.data['data']
        exp_time = parse(response_data['expiryDate'])
        schedule = saved_flight_with_days_to_flight_btw_7_and_29.schedule
        time_diff = schedule - exp_time

        assert response.status_code == 201
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages['booking_success']
        assert time_diff == timedelta(hours=24)

    def test_book_flight_with_days_to_flight_btw_4_and_6_succeeds(
            self, client, saved_flight_with_days_to_flight_btw_4_and_6,
            saved_valid_user_one, valid_user_one_token):
        """Should book flight when the days to flight btw 4 and 6

        The expiryDate in this case should be set to 24 hours after the booking

        Returns:
            None
        """
        valid_flight_id = str(saved_flight_with_days_to_flight_btw_4_and_6.id)
        response = client.post(
            '/api/v1/flight/{}/booking'.format(valid_flight_id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_body = response.data
        response_data = response.data['data']
        exp_time = parse(response_data['expiryDate'])
        created_at = parse(response_data['createdAt'])
        time_diff = exp_time - created_at

        assert response.status_code == 201
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages['booking_success']
        assert timedelta(hours=24) == time_diff

    def test_book_flight_with_days_to_flight_btw_2_and_3_succeeds(
            self, client, saved_flight_with_days_to_flight_btw_2_and_3,
            saved_valid_user_one, valid_user_one_token):
        """Should book flight when the days to flight btw 2 and 3

        The expiryDate in this case should be set to 12 hours after the booking

        Returns:
            None
        """
        valid_flight_id = str(saved_flight_with_days_to_flight_btw_2_and_3.id)
        response = client.post(
            '/api/v1/flight/{}/booking'.format(valid_flight_id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_body = response.data
        response_data = response.data['data']
        exp_time = parse(response_data['expiryDate'])
        created_at = parse(response_data['createdAt'])
        time_diff = exp_time - created_at

        assert response.status_code == 201
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages['booking_success']
        assert timedelta(hours=12) == time_diff

    def test_book_flight_with_hours_to_flight_btw_1_and_24_succeeds(
            self, client, saved_flight_with_hours_to_flight_btw_1_and_6,
            saved_valid_user_one, valid_user_one_token):
        """Should book flight when the days to flight btw 2 and 3

        The expiryDate in this case should be set to 12 hours after the booking

        Returns:
            None
        """
        valid_flight_id = str(saved_flight_with_hours_to_flight_btw_1_and_6.id)
        response = client.post(
            '/api/v1/flight/{}/booking'.format(valid_flight_id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_body = response.data
        response_data = response.data['data']
        exp_time = parse(response_data['expiryDate'])
        created_at = parse(response_data['createdAt'])
        time_diff = exp_time - created_at

        assert response.status_code == 201
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages['booking_success']
        assert timedelta(hours=6) == time_diff

    def test_book_expired_flight_fails(self, client, valid_user_one_token,
                                       saved_valid_user_one,
                                       saved_expired_flight_one):
        valid_flight_id = str(saved_expired_flight_one.id)
        response = client.post(
            '/api/v1/flight/{}/booking'.format(valid_flight_id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        response_body = response.data
        assert response.status_code == 400
        assert response_body['status'] == 'error'
        assert response_body['message'] == serialization_errors[
            'flight_schedule_expired']

    def test_book_flight_twice_fails(self, client, valid_user_one_token,
                                     saved_valid_user_one,
                                     saved_valid_flight_model_one):
        valid_flight_id = str(saved_valid_flight_model_one.id)
        client.post(
            '/api/v1/flight/{}/booking'.format(valid_flight_id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        response = client.post(
            '/api/v1/flight/{}/booking'.format(valid_flight_id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        response_body = response.data
        assert response.status_code == 409
        assert response_body['status'] == 'error'
        assert response_body['message'] == serialization_errors[
            'user_book_flight_twice']

    # POST
    def test_book_flight_with_invalid_token_fails(
            self, client, saved_valid_flight_model_one):
        valid_flight_id = str(saved_valid_flight_model_one.id)

        response = client.post(
            '/api/v1/flight/{}/booking'.format(valid_flight_id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format('invalid-token'),
        )

        assert_token_is_invalid(response)

    def test_book_flight_with_invalid_token_format_fails(
            self, client, valid_user_one_token, saved_valid_flight_model_one):
        valid_flight_id = str(saved_valid_flight_model_one.id)
        response = client.post(
            '/api/v1/flight/{}/booking'.format(valid_flight_id),
            content_type='application/json',
            HTTP_AUTHORIZATION='{}'.format(valid_user_one_token),
        )

        assert_invalid_token_format(response)

    def test_book_flight_with_expired_token_format_fails(
            self, client, expired_token_for_user_one,
            saved_valid_flight_model_one):
        valid_flight_id = str(saved_valid_flight_model_one.id)
        response = client.post(
            '/api/v1/flight/{}/booking'.format(valid_flight_id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(expired_token_for_user_one),
        )

        assert_expired_token(response)

    def test_book_fligh_with_invalid_flight_id_format_fails(
            self, client, valid_user_one_token, saved_valid_flight_model_one):
        invalid_uuid = 'invalid-uuid'
        response = client.post(
            '/api/v1/flight/{}/booking'.format(invalid_uuid),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        assert_resource_not_found(response, 'Flight', invalid_uuid)

    def test_book_fligh_with_valid_uuid_that_is_not_a_flight_id_fails(
            self, client, valid_user_one_token, saved_valid_flight_model_one):
        valid_uuid_not_in_db = uuid4()

        response = client.post(
            '/api/v1/flight/{}/booking'.format(valid_uuid_not_in_db),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )
        assert_resource_not_found(response, 'Flight', valid_uuid_not_in_db)
