from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
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
    def post(request, format='json'):
        """Creates a new flight

        Args:
            request: An object that contains the request made by the user
            format(str): Specifies that JSON is sent to the app

        Returns:
            None

        """
        user = request.decoded_user
        request_data = dict(**request.data, createdBy=user.id)
        serializer = FlightSerializer(data=request_data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()

            return generate_response(
                serializer.data,
                success_messages['resource_created'].format('Flight'),
                status_code=HTTP_201_CREATED)
        raise_error(
            serialization_errors['many_invalid_fields'],
            err_dict=serializer.errors)

    @staticmethod
    def get(request, format='json'):
        queryset = Flight.objects.order_by('-schedule')
        paginator, page = parse_paginator_request_query(
            request.query_params, queryset)
        meta, current_page_data = generate_pagination_meta(paginator, page)
        paginated_data = FlightSerializer(current_page_data, many=True).data

        paginated_response = generate_response(
            paginated_data,
            success_messages['retrieved'].format('Flights'),
            meta=meta)

        return paginated_response


class SingleFlightView(APIView):

    permission_classes = [TokenValidator]
    protected_methods = ['GET']

    @staticmethod
    def get(request, *args, **kwargs):

        flight_id = kwargs.get('id')
        try:
            flight = Flight.objects.filter(id=flight_id).first()
            if not flight:
                raise ValidationError('')
        except ValidationError:
            raise_error('Not found', status_code=HTTP_404_NOT_FOUND)

        json_flight = FlightSerializer(flight).data

        return generate_response(
            json_flight, success_messages['retrieved'].format('Flight'))
