from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST', 'PATCH', 'DELETE', 'PUT'])
def catch_all(request):
    return Response({'message': 'The resource you specified does not exist'})


@api_view(['GET', 'POST', 'PATCH', 'DELETE', 'PUT'])
def welcome_message(request):
    return Response({'message': 'Welcome to the Airtech API!!!'})
