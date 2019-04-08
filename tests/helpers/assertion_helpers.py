"""Module contains assertions used in tests. Each takes a response object"""

from airtech_api.utils.error_messages import tokenization_errors


def assert_missing_header(response):
    response_body = response.data
    assert response.status_code == 401  # unauthorized
    assert response_body['status'] == 'error'
    assert response_body['message'] == tokenization_errors['missing_token']


def assert_invalid_token_format(response):
    response_body = response.data
    assert response.status_code == 401  # unauthorized
    assert response_body['status'] == 'error'
    assert response_body['message'] == tokenization_errors[
        'token_format_error']


def assert_forbidden_user(response):
    response_body = response.data

    assert response.status_code == 403  # forbidden
    assert response_body['status'] == 'error'
    assert response_body['message'] == tokenization_errors['user_is_forbidden']


def assert_token_is_invalid(response):
    response_body = response.data

    assert response.status_code == 401  # unauthorized
    assert response_body['status'] == 'error'
    assert response_body['message'] == tokenization_errors['token_is_invalid']
