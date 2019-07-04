import pytest
import requests
from airtech_api.utils import success_messages
from mock import Mock
from airtech_api.utils.constants import PAYSTACK_INITIALIZE_URL
from airtech_api.utils.error_messages import serialization_errors
from airtech_api.booking.models import Booking
from django.utils import timezone
from tests.helpers.assertion_helpers import assert_missing_header, assert_invalid_token_format
from datetime import datetime
from dateutil.parser import parse
USER_BOOKING_URL = '/api/v1/user/bookings/{}/payment'


class RequestsResponseMock:
    def __init__(self,
                 status_code,
                 raise_exception=False,
                 exception_msg='An error occured',
                 **kwargs):
        if raise_exception:
            raise Exception(exception_msg)
        self._json = kwargs
        self.status_code = status_code

    def json(self):
        return self._json


@pytest.mark.django_db
class TestPayForFlightTicketRoute:
    def test_user_pays_for_booking_ticket_succeeds(
            self, client, valid_user_one_token, saved_valid_user_one,
            saved_bulk_inserted_bookings_for_user_one):

        booking = saved_bulk_inserted_bookings_for_user_one[0]
        booking.paid_at = None
        booking.save()

        paystack_res_mock = {
            'status': True,
            'data': {
                'status': 'success',
                'gateway_response': 'Payment was made to account',
                'metadata': {
                    'callbackURL': 'https://test.com',
                    'bookingId': 'booking-UUID'
                },
            }
        }

        paystack_res_mock = {
            'status': True,
            'data': {
                'authorization_url': 'http://payment-link.com',
            }
        }
        paystack_response = RequestsResponseMock(200, False,
                                                 **paystack_res_mock)
        requests.post = Mock(return_value=paystack_response)

        client_callback = 'https://test.com'
        response = client.post(
            USER_BOOKING_URL.format(booking.id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
            data={
                'callbackURL': client_callback,
            })
        response_body = response.data
        response_data = response_body['data']
        (url, ), res = requests.post.call_args

        data = res['data']

        # Reqeust Assetions
        assert response.status_code == 200
        assert response_body['status'] == 'success'
        assert response_body['message'] == success_messages[
            'payment_url_created']
        assert response_data['paymentLink'] == paystack_res_mock['data'][
            'authorization_url']

        metadata = eval(data['metadata'])
        # Post call assertions
        assert url == PAYSTACK_INITIALIZE_URL
        assert data['amount'] == booking.ticket_price
        assert data['email'] == booking.created_by.email
        assert metadata['callbackURL'] == client_callback
        assert metadata['bookingId'] == str(booking.id)
        assert metadata['username'] == saved_valid_user_one.username
        assert metadata['email'] == saved_valid_user_one.email

    def test_user_pays_for_ticket_that_has_already_been_bought_fails(
            self, client, valid_user_one_token,
            saved_bulk_inserted_bookings_for_user_one):

        booking = saved_bulk_inserted_bookings_for_user_one[0]
        booking.paid_at = timezone.now()
        booking.save()

        paystack_res_mock = {
            'status': True,
            'data': {
                'authorization_url': 'http://payment-link.com',
            }
        }
        paystack_response = RequestsResponseMock(200, False,
                                                 **paystack_res_mock)
        requests.post = Mock(return_value=paystack_response)

        client_callback = 'https://test.com'
        response = client.post(
            USER_BOOKING_URL.format(booking.id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
            data={
                'callbackURL': client_callback,
            })
        response_body = response.data

        # Reqeust Assetions
        assert response.status_code == 400
        assert response_body['status'] == 'error'
        assert response_body['message'] == serialization_errors[
            'booking_already_paid']
        assert requests.post.called is False

    def test_user_pays_for_ticket_that_is_expired_fails(
            self, client, valid_user_one_token, expired_booking):
        paystack_res_mock = {
            'status': True,
            'data': {
                'authorization_url': 'http://payment-link.com',
            }
        }
        paystack_response = RequestsResponseMock(200, False,
                                                 **paystack_res_mock)
        requests.post = Mock(return_value=paystack_response)

        client_callback = 'https://test.com'
        response = client.post(
            USER_BOOKING_URL.format(expired_booking.id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
            data={
                'callbackURL': client_callback,
            })
        response_body = response.data

        # Reqeust Assetions
        assert response.status_code == 400
        assert response_body['status'] == 'error'
        assert response_body['message'] == serialization_errors[
            'booking_expired']
        assert requests.post.called is False

    def test_make_payment_with_invalid_callback_url_fails(
            self, client, valid_user_one_token,
            saved_bulk_inserted_bookings_for_user_one):
        booking = saved_bulk_inserted_bookings_for_user_one[0]
        paystack_res_mock = {
            'status': True,
            'data': {
                'authorization_url': 'http://payment-link.com',
            }
        }
        paystack_response = RequestsResponseMock(200, False,
                                                 **paystack_res_mock)
        requests.post = Mock(return_value=paystack_response)

        client_callback = 'utc://test.com'
        response = client.post(
            USER_BOOKING_URL.format(booking.id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
            data={
                'callbackURL': client_callback,
            })
        response_body = response.data

        # Reqeust Assetions
        assert response.status_code == 400
        assert response_body['status'] == 'error'
        assert response_body['message'] == serialization_errors[
            'invalid_url'].format('callbackURL')
        assert requests.post.called is False

    def test_payment_fails_when_paystack_throws_an_error(
            self, client, valid_user_one_token,
            saved_bulk_inserted_bookings_for_user_one):
        booking = saved_bulk_inserted_bookings_for_user_one[0]

        requests.post = Mock(return_value=Exception())

        client_callback = 'https://test.com'
        response = client.post(
            USER_BOOKING_URL.format(booking.id),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
            data={
                'callbackURL': client_callback,
            })
        response_body = response.data

        # Reqeust Assetions
        assert response.status_code == 400
        assert response_body['status'] == 'error'
        assert response_body['message'] == serialization_errors[
            'payment_link_error']
        assert requests.post.called

    def test_make_payment_without_invalid_token_fails(
            self, client, saved_bulk_inserted_bookings_for_user_one):
        booking = saved_bulk_inserted_bookings_for_user_one[0]

        response = client.post(
            USER_BOOKING_URL.format(booking.id),
            content_type='application/json',
            HTTP_AUTHORIZATION='{}'.format('invalid-token'),
        )

        assert_invalid_token_format(response)

    def test_make_payment_with_missing_token_fails(
            self, client, saved_bulk_inserted_bookings_for_user_one):
        booking = saved_bulk_inserted_bookings_for_user_one[0]

        response = client.post(
            USER_BOOKING_URL.format(booking.id),
            content_type='application/json',
        )
        assert_missing_header(response)


@pytest.mark.django_db
class TestPaymentRedirectRoute:
    def test_get_call_raises_an_exception(
            self, client, saved_bulk_inserted_bookings_for_user_one):
        booking = saved_bulk_inserted_bookings_for_user_one[0]

        requests.get = Mock(side_effect=Exception())
        response = client.get(
            USER_BOOKING_URL.format(booking.id) + '?reference=blah')

        assert response.status_code == 400
        assert response.data['status'] == 'error'
        assert response.data['message'] == \
               serialization_errors['paystack_threw_error']

    def test_paystack_returns_failure_when_verifying_user(
            self, client, saved_bulk_inserted_bookings_for_user_one):
        booking = saved_bulk_inserted_bookings_for_user_one[0]
        booking.paid_at = None
        booking.save()

        payment_time = datetime.now()
        client_callback = 'https://test.com'
        paystack_res_mock = {
            'status': False,
            'data': {
                'status': 'failure',
                'gateway_response': 'Payment was made to account',
                'paid_at': payment_time,
                'metadata': {
                    'callbackURL': client_callback,
                    'bookingId': str(booking.id)
                },
            }
        }
        paystack_response = RequestsResponseMock(200, False,
                                                 **paystack_res_mock)
        requests.get = Mock(return_value=paystack_response)
        reference_mock = 'reference-101'
        response = client.get(
            USER_BOOKING_URL.format(booking.id) +
            f'?reference={reference_mock}', )
        query_params = {
            query.split('=')[0]: query.split('=')[1]
            for query in response.url.split('?')[1].split('&')
        }

        assert response.status_code == 303
        assert response.url.startswith(client_callback)
        assert query_params['success'] == 'false'
        assert query_params['bookingId'] == str(booking.id)

    def test_paystack_returns_insufficient_funds_error(
            self, client, saved_bulk_inserted_bookings_for_user_one):
        booking = saved_bulk_inserted_bookings_for_user_one[0]
        booking.paid_at = None
        booking.save()

        payment_time = datetime.now()
        client_callback = 'https://test.com'
        paystack_res_mock = {
            'status': True,
            'data': {
                'status': 'failure',
                'gateway_response': 'Insufficient funds',
                'paid_at': payment_time,
                'metadata': {
                    'callbackURL': client_callback,
                    'bookingId': str(booking.id)
                },
            }
        }
        paystack_response = RequestsResponseMock(200, False,
                                                 **paystack_res_mock)
        requests.get = Mock(return_value=paystack_response)
        reference_mock = 'reference-101'
        response = client.get(
            USER_BOOKING_URL.format(booking.id) +
            f'?reference={reference_mock}', )
        query_params = {
            query.split('=')[0]: query.split('=')[1]
            for query in response.url.split('?')[1].split('&')
        }

        assert response.status_code == 303
        assert response.url.startswith(client_callback)
        assert query_params['success'] == 'false'
        assert query_params['bookingId'] == str(booking.id)

    def test_successful_payment_redirects_user_succeeds(
            self, client, valid_user_one_token, saved_valid_user_one,
            saved_bulk_inserted_bookings_for_user_one):

        booking = saved_bulk_inserted_bookings_for_user_one[0]
        booking.paid_at = None
        booking.save()
        payment_time = timezone.now()
        client_callback = 'https://test.com'
        paystack_res_mock = {
            'status': True,
            'data': {
                'status': 'success',
                'gateway_response': 'Payment was made to account',
                'paid_at': payment_time,
                'metadata': {
                    'callbackURL': client_callback,
                    'bookingId': str(booking.id)
                },
            }
        }
        paystack_response = RequestsResponseMock(200, False,
                                                 **paystack_res_mock)
        requests.get = Mock(return_value=paystack_response)

        reference_mock = 'sample-reference'

        response = client.get(
            USER_BOOKING_URL.format(booking.id) +
            f'?reference={reference_mock}',
            # content_type='application/json',
        )

        query_params = {
            query.split('=')[0]: query.split('=')[1]
            for query in response.url.split('?')[1].split('&')
        }
        booking = Booking.objects.get(pk=booking.id)

        # Reqeust Assetions
        assert response.status_code == 303
        assert query_params['success'] == 'true'
        assert query_params['bookingId'] == str(booking.id)
        assert response.url.startswith(client_callback)
        assert booking.paid_at == payment_time
