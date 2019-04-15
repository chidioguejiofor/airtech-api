from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_409_CONFLICT
from ..utils.helpers.json_helpers import (generate_response, raise_error,
                                          retrieve_model_with_id,
                                          parse_paginator_request_query,
                                          generate_pagination_meta)

from .serializers import BookingSerializer
from ..utils.error_messages import serialization_errors
from ..utils.validators.token_validator import TokenValidator
from ..utils import success_messages
from ..flight.models import Flight

from .models import Booking


class BookingView(APIView):

    permission_classes = [TokenValidator]
    protected_methods = ['POST', 'GET']

    def post(self, request, **kwargs):
        flight_id = kwargs.get('flight_id', '')
        flight = retrieve_model_with_id(
            Flight,
            flight_id,
            serialization_errors['resource_id_not_found'].format(
                'Flight', flight_id),
        )
        request_body = {
            'ticket_price': flight.current_price,
            'flight_model': flight.id,
            'created_by': request.decoded_user.id,
        }

        serializer = BookingSerializer(data=request_body)

        if serializer.is_valid(raise_exception=False):

            serializer.save()
            return generate_response(serializer.data,
                                     success_messages['booking_success'],
                                     status_code=HTTP_201_CREATED)
        if 'non_field_errors' in serializer.errors:

            raise_error(serialization_errors['user_book_flight_twice'],
                        status_code=HTTP_409_CONFLICT)

        raise_error(serializer.errors['flight_model'][0])

    def get(self, request):
        return generate_response('Hello', 'Hi')


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
            paginated_data,
            success_messages['retrieved'].format('Bookings'),
            meta=meta)

        return paginated_response
