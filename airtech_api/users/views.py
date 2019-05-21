# Create your views here.

from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from ..utils.helpers.json_helpers import generate_response, raise_error, add_token_to_response
from ..utils import success_messages
from ..utils.error_messages import serialization_errors, tokenization_errors
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from ..utils.validators.token_validator import TokenValidator
from ..utils.constants import CONFIRM_EMAIL_TYPE
from django.http import HttpResponseRedirect
from .models import User
from rest_framework.decorators import api_view

from ..utils.helpers.email_helpers import send_confirm_mail


class SignupView(APIView):
    def post(self, request):
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
            user_email = serialization_data['email']
            server_host = request.get_host()
            client_host = request.headers.get('Host')
            send_confirm_mail(user_email, server_host, client_host)
            return generate_response(
                success_messages['confirm_mail'].format(user_email),
                status_code=HTTP_201_CREATED)
        raise_error(serialization_errors['many_invalid_fields'],
                    err_dict=serializer.errors)


class ConfirmView(APIView):
    def get(self, request, **kwargs):
        token = kwargs.get('token', '')
        decoded = TokenValidator.decode_token(token)
        type_is_not_valid = decoded.get('type') != CONFIRM_EMAIL_TYPE
        email_is_not_valid = 'email' not in decoded
        if type_is_not_valid or email_is_not_valid:
            raise_error(tokenization_errors['token_is_invalid'],
                        HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(email=decoded['email']).first()
        if not user:
            raise_error(tokenization_errors['token_is_invalid'],
                        HTTP_401_UNAUTHORIZED)

        user.verified = True
        user.save()
        return HttpResponseRedirect(redirect_to=decoded.get('redirect_url'))


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
                success_messages['auth_successful'].format('Login'),
                serialization_data)

        if 'non_field_errors' in serializer.errors.keys():
            raise_error(serialization_errors['user_not_found'],
                        status_code=HTTP_404_NOT_FOUND)

        raise_error(serialization_errors['many_invalid_fields'],
                    err_dict=serializer.errors)


@api_view(['POST'])
def resend_email(request):

    email = request.data.get('email')
    user = User.objects.filter(email=email).first()
    server_host = request.get_host()
    client_host = request.headers.get('Host')

    if not user:
        raise_error(serialization_errors['email_not_found'].format(email),
                    status_code=HTTP_404_NOT_FOUND)
    elif user.verified:
        raise_error(serialization_errors['user_already_verified'])

    send_confirm_mail(user.email, server_host, client_host)
    return generate_response(success_messages['confirm_mail'].format(email))
