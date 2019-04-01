import os
import jwt
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


def generate_response(response_data, message, status_code=HTTP_200_OK):
    return Response(
        data={
            'status': 'success',
            'message': message,
            'data': response_data,
        },
        status=status_code)


def raise_error(message,
                status_code=HTTP_400_BAD_REQUEST,
                err_dict=None,
                raise_only_message=False):
    err_obj = {'status': 'error', 'message': message}
    if not raise_only_message and isinstance(err_dict, dict):
        err_obj.setdefault('errors', err_dict)

    error_detail = message if raise_only_message else err_obj
    api_exception = serializers.ValidationError(error_detail)

    api_exception.status_code = status_code
    raise api_exception


def clean_up_user_data(user_data):
    """Clean up response sent to users

    Removes password field and adds token to user data

    Args:
        user_data: The user data to be passed

    Returns:

    """
    del user_data['password']
    user_data['token'] = jwt.encode(
        user_data,
        os.getenv('JWT_SCRET_KEY'),
    )
    return user_data