# Create your views here.

from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from ..utils.helpers.json_helpers import generate_response, raise_error, add_token_to_response
from ..utils import success_messages
from ..utils.error_messages import serialization_errors
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND


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

            serialization_data = add_token_to_response(serializer.data)

            return generate_response(
                serialization_data,
                success_messages['auth_successful'].format('Sign Up'),
                status_code=HTTP_201_CREATED)

        raise_error(
            serialization_errors['many_invalid_fields'],
            err_dict=serializer.errors)


class LoginView(APIView):
    def post(self, request, format='json'):
        """
        Saves a new user to the app

        Returns:
            A Response object containing the JSON response
        """
        request_data = dict(**request.data)
        serializer = LoginSerializer(data=request_data)

        if serializer.is_valid(raise_exception=False):
            user = serializer.validated_data
            serialized_user = UserSerializer(user).data
            serialization_data = add_token_to_response(serialized_user)

            return generate_response(
                serialization_data,
                success_messages['auth_successful'].format('Login'),
                status_code=HTTP_200_OK)

        if 'non_field_errors' in serializer.errors.keys():
            raise_error(
                serialization_errors['user_not_found'],
                status_code=HTTP_404_NOT_FOUND)

        raise_error(
            serialization_errors['many_invalid_fields'],
            err_dict=serializer.errors)
