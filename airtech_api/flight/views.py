from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from django.utils import timezone
from ..utils.helpers.json_helpers import (generate_response, raise_error,
                                          generate_pagination_meta,
                                          parse_paginator_request_query)
from .serializers import FlightSerializer
from ..utils.error_messages import serialization_errors
from ..utils.validators.token_validator import AdminTokenValidator, TokenValidator
from ..utils import success_messages
from .models import Flight


class FlightView(APIView):

    permission_classes = [AdminTokenValidator]
    protected_methods = ['POST', 'GET']
    regular_user_methods = ['GET']

    @staticmethod
    def post(request):
        user = request.decoded_user
        request_data = dict(**request.data, created_by=user.id)
        serializer = FlightSerializer(data=request_data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()

            return generate_response(
                success_messages['resource_created'].format('Flight'),
                serializer.data,
                status_code=HTTP_201_CREATED)
        raise_error(serialization_errors['many_invalid_fields'],
                    err_dict=serializer.errors)

    @staticmethod
    def get(request):
        queryset = Flight.objects.order_by('-schedule')
        paginator, page = parse_paginator_request_query(
            request.query_params, queryset)
        meta, current_page_data = generate_pagination_meta(paginator, page)
        paginated_data = FlightSerializer(current_page_data, many=True).data

        paginated_response = generate_response(
            success_messages['retrieved'].format('Flights'),
            paginated_data,
            meta=meta)

        return paginated_response


class SingleFlightView(APIView):

    permission_classes = [AdminTokenValidator]
    protected_methods = ['GET', 'DELETE', 'PATCH']
    regular_user_methods = ['GET']

    @staticmethod
    def get(request, *args, **kwargs):
        flight_id = kwargs.get('id')
        flight = Flight.get_model_by_id_or_404(flight_id)
        json_flight = FlightSerializer(flight).data

        return generate_response(
            success_messages['retrieved'].format('Flight'),
            json_flight,
        )

    @staticmethod
    def delete(request, **kwargs):
        id = kwargs.get('id', '')
        flight = Flight.get_model_by_id_or_404(id)
        number_of_bookings = flight.bookings.count()
        if timezone.now() >= flight.schedule:
            raise_error(
                serialization_errors['cannot_delete_flight_that_has_flown'], )
        if number_of_bookings > 0:
            raise_error(
                serialization_errors['cannot_delete_flight_with_bookings'], )

        flight_id = flight.id
        flight.delete()
        return generate_response(
            success_messages['deleted'].format('Flight', flight_id), )

    @staticmethod
    def patch(request, *args, **kwargs):
        flight_id = kwargs.get('id')
        flight = Flight.get_model_by_id_or_404(flight_id)
        user_request = request.data
        return FlightSerializer.update_data_from_requests(user_request, flight)
