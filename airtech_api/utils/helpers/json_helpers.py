import os
import jwt
from django.core.paginator import Paginator
from ..constants import DEFAULT_ITEMS_PER_PAGE
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from datetime import datetime, timedelta
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def generate_response(message,
                      response_data=None,
                      status_code=HTTP_200_OK,
                      meta=None):
    data = {
        'status': 'success',
        'message': message,
    }
    if response_data is not None:
        data['data'] = response_data
    if isinstance(meta, dict):
        data['meta'] = meta

    return Response(data=data, status=status_code)


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


def add_token_to_response(user_data, exp=None):
    """Clean up response sent to users

    Removes password field and adds token to user data

    Args:
        user_data: The user data to be passed
        exp: The expiry date
    Returns:

    """
    token_data = {
        'id': user_data['id'],
        'username': user_data['username'],
        'email': user_data['email'],
    }

    if exp:
        token_data['exp'] = exp
    user_data['token'] = generate_token(token_data)
    return user_data


def generate_token(token_data):
    """Returns a decodes a dict into a token

    Args:
        token_data: the data to be tokenized
    Returns:

    """
    if 'exp' not in token_data:
        token_data['exp'] = datetime.utcnow() + timedelta(minutes=30)
    return jwt.encode(token_data,
                      os.getenv('JWT_SCRET_KEY'),
                      algorithm='HS256').decode('ascii')


def generate_pagination_meta(paginator, page):
    page_data = paginator.page(page)
    meta = {
        'totalPages': paginator.num_pages,
        'currentPage': page,
        'nextPageNumber': None,
        'previousPageNumber': None,
        'itemsPerPage': paginator.per_page
    }
    if page_data.has_next():
        meta['nextPageNumber'] = page_data.next_page_number()
    if page_data.has_previous():
        meta['previousPageNumber'] = page_data.previous_page_number()

    return meta, page_data


def parse_paginator_request_query(query_params, queryset):

    limit = query_params.get('limit', DEFAULT_ITEMS_PER_PAGE)
    page = query_params.get('page', '1')

    limit = int(limit) if limit.isdigit() else 10
    page = int(page) if page.isdigit() else 1

    limit_is_btw_1_and_20_inclusive = limit >= 1 and limit <= 20

    limit = limit if limit_is_btw_1_and_20_inclusive else int(
        DEFAULT_ITEMS_PER_PAGE)
    paginator = Paginator(queryset, limit)
    total_pages = paginator.num_pages
    page = total_pages if page > total_pages else page

    return paginator, page


def retrieve_model_with_id(model, model_id, *err_args, **err_kwargs):
    try:
        model_instance = model.objects.filter(id=model_id).first()
        if not model_instance:
            raise ValidationError('')
    except ValidationError:
        raise_error(*err_args, HTTP_404_NOT_FOUND, **err_kwargs)

    return model_instance
