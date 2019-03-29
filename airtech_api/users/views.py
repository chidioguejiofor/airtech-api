# Create your views here.

from rest_framework.views import APIView
from .serializers import UserSerializer
from ..utils.helpers.json_helpers import generate_response, raise_error
from ..utils.success_messages import signup_route
from ..utils.error_messages import serialization_errors
from rest_framework.status import HTTP_201_CREATED


class SignupView(APIView):
    def post(self, request, format='json'):
        """
        Saves a new user to the app

        Returns:
            A Response object containing the JSON response
        """
        request_data = dict(**request.data)
        serializer = UserSerializer(data=request_data)

        if serializer.is_valid():
            _ = serializer.save()

            serialization_data = serializer.data
            serialization_data.pop('password', False)
            return generate_response(
                serialization_data,
                signup_route['signup_success'],
                status_code=HTTP_201_CREATED)

        raise_error(
            serialization_errors['many_invalid_fields'],
            err_dict=serializer.errors)
