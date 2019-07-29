from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_409_CONFLICT
import requests
import os
from django.http import QueryDict
import json
from django.core.validators import URLValidator
from ..utils.helpers.json_helpers import (generate_response, raise_error,
                                          parse_paginator_request_query,
                                          generate_pagination_meta)

from .serializers import BookingSerializer
from ..utils.error_messages import serialization_errors
from ..utils.validators.token_validator import TokenValidator
from ..utils import success_messages
from ..flight.models import Flight
from ..utils.constants import PAYSTACK_INITIALIZE_URL
from .models import Booking


class BookingView(APIView):

    permission_classes = [TokenValidator]
    protected_methods = ['POST', 'GET']

    def post(self, request, **kwargs):
        flight_id = kwargs.get('flight_id', '')
        flight = Flight.get_model_by_id_or_404(flight_id)
        request_body = {
            'ticket_price': flight.current_price,
            'flight_model': flight.id,
            'created_by': request.decoded_user.id,
        }

        serializer = BookingSerializer(data=request_body)

        if serializer.is_valid(raise_exception=False):

            serializer.save()
            return generate_response(success_messages['booking_success'],
                                     serializer.data,
                                     status_code=HTTP_201_CREATED)
        if 'non_field_errors' in serializer.errors:

            raise_error(serialization_errors['user_book_flight_twice'],
                        status_code=HTTP_409_CONFLICT)

        raise_error(serializer.errors['flight_model'][0])


class SingleUserBookings(APIView):
    permission_classes = [TokenValidator]
    protected_methods = ['DELETE', 'GET']

    def delete(self, request, **kwargs):
        id = kwargs.get('id', '')
        extra_filter = {'created_by': request.decoded_user}
        booking = Booking.get_model_by_id_or_404(id,
                                                 extra_filters=extra_filter)
        if booking.paid_at:
            raise_error(
                serialization_errors['paid_booking_cannot_be_deleted'], )
        if booking.has_expired():
            raise_error(
                serialization_errors['cannot_delete_expired_booking'], )
        booking_id = str(booking.id)
        booking.delete()

        return generate_response(
            success_messages['deleted'].format('Booking', booking_id), )


class UserBookings(APIView):
    permission_classes = [TokenValidator]
    protected_methods = ['GET']

    def get(self, request):
        queryset = Booking.objects.filter(
            created_by=request.decoded_user.id).order_by('-created_at')

        paginator, page = parse_paginator_request_query(
            request.query_params, queryset)

        meta, current_page_data = generate_pagination_meta(paginator, page)
        serialized = BookingSerializer(current_page_data, many=True)
        serialized.child.fields.pop('bookedBy')
        paginated_data = serialized.data

        paginated_response = generate_response(
            success_messages['retrieved'].format('Bookings'),
            paginated_data,
            meta=meta)

        return paginated_response


class UserPayment(APIView):
    permission_classes = [TokenValidator]
    protected_methods = ['POST']

    def get(self, request, id):
        reference = request.query_params['reference']
        response = None
        try:
            response = requests.get(
                f'https://api.paystack.co/transaction/verify/{reference}',
                headers={
                    "Authorization":
                    "Bearer {}".format(os.getenv('PAYSTACK_SECRET'))
                })
        except Exception:
            raise_error(serialization_errors['paystack_threw_error'])

        payment_details = response.json()
        payment_data = payment_details['data']
        metadata = payment_data['metadata']
        callback_url = metadata.get("callbackURL", "/")
        if not payment_details['status']:
            redirect_url = self.generate_redirect_url(
                callback_url,
                success='false',
                bookingId=metadata['bookingId'],
                message=payment_details.get('message', 'An error occured'))
        elif payment_data['status'] != 'success':
            redirect_url = self.generate_redirect_url(
                callback_url,
                success='false',
                bookingId=metadata['bookingId'],
                message=payment_data['gateway_response'])
        else:
            booking = Booking.get_model_by_id_or_404(metadata['bookingId'])
            booking.paid_at = payment_data['paid_at']
            booking.save()
            redirect_url = self.generate_redirect_url(
                callback_url,
                success='true',
                bookingId=metadata['bookingId'],
                message=payment_data.get('gateway_response',
                                         'Payment Successful'))
        return HttpResponseRedirect(redirect_to=redirect_url, status=303)

    @staticmethod
    def generate_redirect_url(callback_url, *args, **kwargs):
        q = QueryDict(mutable=True)
        for query_string, value in kwargs.items():
            q[query_string] = value
        query_string = q.urlencode()
        return f'{callback_url}?{query_string}'

    @staticmethod
    def post(request, id):
        user = request.decoded_user

        filter_args = dict(created_by=user.id)
        booking = Booking.get_model_by_id_or_404(id, filter_args)

        if booking.paid_at:
            raise_error(serialization_errors['booking_already_paid'])

        if booking.has_expired():
            raise_error(serialization_errors['booking_expired'])

        callback_url = request.data.get('callbackURL')
        try:
            validate = URLValidator(schemes=['http', 'https'])
            validate(callback_url)
        except Exception as e:
            raise_error(
                'The `callbackURL` field must be a valid URL with protocols `http` or `https`'
            )

        try:
            response = requests.post(
                PAYSTACK_INITIALIZE_URL,
                data={
                    'amount':
                    booking.ticket_price,
                    'email':
                    user.email,
                    'metadata':
                    json.dumps({
                        'bookingId': str(booking.id),
                        'username': user.username,
                        'email': user.email,
                        'callbackURL': callback_url,
                    }),
                    'callback_url':
                    f'http://{request.get_host()}/api/v1/user/bookings/{id}/payment'
                },
                headers={
                    "Authorization":
                    "Bearer {}".format(os.getenv('PAYSTACK_SECRET'))
                })
            data = response.json()['data']
            return generate_response(
                success_messages['payment_url_created'],
                {'paymentLink': data['authorization_url']},
                200,
            )
        except Exception:
            raise_error(serialization_errors['payment_link_error'])
