# Create your views here.

from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from ..utils.helpers.json_helpers import generate_response, raise_error, add_token_to_response, validate_url, validate_confirmation_request
from ..utils import success_messages
from ..utils.error_messages import serialization_errors, tokenization_errors
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_202_ACCEPTED
from ..utils.validators.token_validator import TokenValidator, VerifiedUserTokenValidator
from ..utils.constants import CONFIRM_EMAIL_TYPE, ADMIN_REQUEST_EMAIL_TYPE, ADMIN_REQUEST_SUBJECT, CONFRIM_EMAIL_SUBJECT
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, JSONParser
from ..utils.helpers.email_helpers import send_email_with_token

from airtech_api.services.cloudinary import upload_profile_picture

from airtech_api.users.models import User
from datetime import datetime, timedelta
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile

import os


class SignupView(APIView):
    @staticmethod
    def post(request):
        """
        Saves a new user to the app

        Returns:
            A Response object containing the JSON response
        """
        request_data = dict(**request.data)
        callback_url = request_data.get('callbackURL', '')

        err_dict = {}
        if not validate_url(callback_url):
            err_dict = {
                'callbackURL': [serialization_errors['invalid_url_field']]
            }

        serializer = UserSerializer(data=request_data)
        if serializer.is_valid() and not err_dict:
            _ = serializer.save()

            serialization_data = serializer.data
            user_email = serialization_data['email']
            server_host = os.getenv('HOSTNAME')
            send_email_with_token(
                user_email,
                'confirm-email.html',
                subject=CONFRIM_EMAIL_SUBJECT,
                redirect_url=callback_url,
                confirm_link=f'{server_host}/api/v1/auth/confirm-email',
                mail_type=CONFIRM_EMAIL_TYPE,
            )
            return generate_response(
                success_messages['confirm_mail'].format(user_email),
                status_code=HTTP_201_CREATED)
        err_dict.update(serializer.errors)
        raise_error(serialization_errors['many_invalid_fields'],
                    err_dict=err_dict)


class ConfirmView(APIView):
    @staticmethod
    def get(request, **kwargs):
        token = kwargs.get('token', '')
        user, redirect_url = validate_confirmation_request(
            token, CONFIRM_EMAIL_TYPE, success_key='verified')
        if user:
            user.verified = True
            user.save()
        return HttpResponseRedirect(redirect_to=redirect_url)


class RequestAdminAccessView(APIView):
    permission_classes = [VerifiedUserTokenValidator]
    protected_methods = ['POST']

    @staticmethod
    def post(request):
        user = request.decoded_user
        callback_url = request.data.get('callbackURL', '')
        if not validate_url(callback_url):
            raise_error(serialization_errors['many_invalid_fields'],
                        err_dict={
                            'callbackURL':
                            [serialization_errors['invalid_url_field']]
                        })

        if user.admin:
            raise_error(serialization_errors['regular_user_only'],
                        status_code=403)
        if not user.image_url:
            raise_error(serialization_errors['profile_not_updated'],
                        status_code=403)

        server_host = os.getenv('HOSTNAME')

        send_email_with_token(
            os.getenv('OWNER_EMAIL'),
            'admin-request-email.html',
            subject=ADMIN_REQUEST_SUBJECT,
            redirect_url=callback_url,
            confirm_link=f'{server_host}/api/v1/auth/request-admin-access',
            mail_type=ADMIN_REQUEST_EMAIL_TYPE,
            first_name=user.first_name,
            last_name=user.last_name,
            user_email=user.email,
            profile_picture=user.image_url,
        )
        return generate_response(success_messages['admin_request_sent'])


class LoginView(APIView):
    @staticmethod
    def post(request):
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
            serialization_data = add_token_to_response(serialized_user,
                                                       exp=datetime.now() +
                                                       timedelta(days=4))

            return generate_response(
                success_messages['auth_successful'].format('Login'),
                serialization_data)

        if 'non_field_errors' in serializer.errors.keys():
            raise_error(serialization_errors['user_not_found'],
                        status_code=HTTP_404_NOT_FOUND)

        raise_error(serialization_errors['many_invalid_fields'],
                    err_dict=serializer.errors)


@api_view(['GET'])
def accept_admin_request(request, **kwargs):
    token = kwargs.get('token', '')
    user, redirect_url = validate_confirmation_request(
        token, ADMIN_REQUEST_EMAIL_TYPE, success_key='admin_approval')

    if user:
        user.admin = True
        user.save()
    return HttpResponseRedirect(redirect_to=redirect_url)


class ResendEmailEndpoint(APIView):
    permission_classes = [TokenValidator]
    protected_methods = ['POST']

    @staticmethod
    def post(request):

        callback_url = request.data.get('callbackURL', '')

        if not validate_url(callback_url):
            raise_error(serialization_errors['many_invalid_fields'],
                        err_dict={
                            'callbackURL':
                            serialization_errors['invalid_url_field']
                        })

        email = request.data.get('email')
        user = request.decoded_user

        if user.verified:
            raise_error(serialization_errors['user_already_verified'])

        server_host = os.getenv('HOSTNAME')
        send_email_with_token(
            user.email,
            'confirm-email.html',
            subject=CONFRIM_EMAIL_SUBJECT,
            redirect_url=callback_url,
            confirm_link=f'{server_host}/api/v1/auth/confirm-email',
            mail_type=CONFIRM_EMAIL_TYPE,
        )
        return generate_response(
            success_messages['confirm_mail'].format(email))


class UserProfilePicture(APIView):
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )
    permission_classes = [TokenValidator]

    @staticmethod
    def patch(request):
        file = request.data.get('picture')
        if not file:
            raise_error(serialization_errors['many_invalid_fields'],
                        err_dict={
                            'picture': serialization_errors['missing_field'],
                        })
        if not isinstance(file, UploadedFile):
            raise_error(serialization_errors['many_invalid_fields'],
                        err_dict={
                            'picture':
                            serialization_errors['value_not_a_file'],
                        })
        user = request.decoded_user
        octet_stream_is_valid = file.content_type == 'application/octet-stream' and os.getenv(
            'ENVIRONMENT') == 'test'
        file_is_image = file.content_type.split('/')[0] == 'image'

        if not octet_stream_is_valid and not file_is_image:
            raise_error(serialization_errors['not_an_image'])

        file_size = file.size
        if file_size > 2_000_000:
            raise_error(serialization_errors['image_too_large'])

        file_name = str(user.id) + datetime.now().strftime('%c') + '.jpg'
        default_storage.save(file_name, ContentFile(file.read()))
        upload_profile_picture.delay(user.id, user.image_public_id, file_name)

        return generate_response('Your request is being processed.',
                                 status_code=HTTP_202_ACCEPTED)
