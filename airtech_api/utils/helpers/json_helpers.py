import os
import jwt
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from datetime import datetime, timedelta


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


def add_token_to_response(user_data):
    """Clean up response sent to users

    Removes password field and adds token to user data

    Args:
        user_data: The user data to be passed

    Returns:

    """
    token_data = {
        'id': user_data['id'],
        'username': user_data['username'],
        'email': user_data['email'],
        'exp': datetime.utcnow() + timedelta(weeks=1)
    }
    user_data['token'] = jwt.encode(
        token_data, os.getenv('JWT_SCRET_KEY'), algorithm='HS256')
    return user_data
