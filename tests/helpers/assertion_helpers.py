"""Module contains assertions used in tests. Each takes a response object"""

from airtech_api.utils.error_messages import tokenization_errors, serialization_errors


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


def assert_expired_token(response):
    response_body = response.data

    assert response.status_code == 401  # unauthorized
    assert response_body['status'] == 'error'
    assert response_body['message'] == tokenization_errors['expired_token']


def assert_resource_not_found(response, resource_name, bad_id):
    response_body = response.data
    assert response.status_code == 404
    assert response_body['status'] == 'error'
    assert response_body['message'] == \
           serialization_errors['resource_id_not_found'].format(
               resource_name
           )


def assert_send_mail_data(message_obj, **kwargs):
    receiever_email = message_obj.personalizations[0].tos[0]['email']
    assert message_obj.subject._subject == kwargs.get('subject')
    assert message_obj.from_email.email == 'no-reply@airtech-api.com'
    assert receiever_email == kwargs.get('receiver')


def assert_redirect_response(response,
                             success_param,
                             client_callback=None,
                             status_code=302):
    query_params = {
        query.split('=')[0]: query.split('=')[1]
        for query in response.url.split('?')[1].split('&')
    }
    if client_callback:
        assert response.url.startswith(client_callback)
    assert response.status_code == status_code
    assert query_params['success'] == success_param
