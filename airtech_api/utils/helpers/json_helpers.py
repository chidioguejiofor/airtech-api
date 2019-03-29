from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.status import HTTP_200_OK


def generate_response(response_data, message, status_code=HTTP_200_OK):
    return Response(
        data={
            'status': 'success',
            'message': message,
            'data': response_data,
        },
        status=status_code)


def raise_error(message, status_code=400, err_dict=None):

    err_obj = {'status': 'error', 'message': message}

    if isinstance(err_dict, dict):
        err_obj.setdefault('errors', err_dict)
    else:
        err_obj = message

    raise serializers.ValidationError(err_obj, code=status_code)
