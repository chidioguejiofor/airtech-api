from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from airtech_api.utils.success_messages import index_route
from airtech_api.utils.error_messages import (not_found_errors)


@api_view(['GET', 'POST', 'PATCH', 'DELETE', 'PUT'])
def catch_all(request):
    return Response({'message': not_found_errors['resource_not_found']},
                    status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PATCH', 'DELETE', 'PUT'])
def welcome_message(request):
    return Response({'message': index_route['welcome_message']})
