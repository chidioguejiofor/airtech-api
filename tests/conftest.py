import pytest
from airtech_api.users.models import User
from airtech_api.flight.models import Flight
from airtech_api.utils.helpers.json_helpers import add_token_to_response
from tests.mocks.users import valid_admin_user, valid_user_one
from tests.mocks.flight import (
    valid_flight_one,
    generate_flight_in_the_future,
)


@pytest.fixture(scope='function')
def saved_valid_user_one(transactional_db):

    user = User(**valid_user_one)
    user.save()
    return user


@pytest.fixture(scope='function')
def saved_valid_admin_user_model_one(transactional_db):

    user = User(**valid_admin_user)
    user.save()
    return user


@pytest.fixture(scope='function')
def saved_valid_flight_model_one(transactional_db,
                                 saved_valid_admin_user_model_one):

    flight = Flight(
        **valid_flight_one, created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


@pytest.fixture(scope='function')
def saved_flight_with_days_to_flight_gt_60(transactional_db,
                                           saved_valid_admin_user_model_one):
    flight = Flight(
        **generate_flight_in_the_future(days=79),
        created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


@pytest.fixture(scope='function')
def saved_flight_with_days_to_flight_btw_30_and_59(
        transactional_db, saved_valid_admin_user_model_one):
    flight = Flight(
        **generate_flight_in_the_future(days=40),
        created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


@pytest.fixture(scope='function')
def saved_flight_with_days_to_flight_btw_7_and_29(
        transactional_db, saved_valid_admin_user_model_one):
    flight = Flight(
        **generate_flight_in_the_future(days=19),
        created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


@pytest.fixture(scope='function')
def saved_flight_with_days_to_flight_btw_4_and_6(
        transactional_db, saved_valid_admin_user_model_one):
    flight = Flight(
        **generate_flight_in_the_future(days=5),
        created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


@pytest.fixture(scope='function')
def saved_flight_with_days_to_flight_btw_2_and_3(
        transactional_db, saved_valid_admin_user_model_one):
    flight = Flight(
        **generate_flight_in_the_future(days=2.5),
        created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


@pytest.fixture(scope='function')
def saved_flight_with_hours_to_flight_btw_1_and_6(
        transactional_db, saved_valid_admin_user_model_one):
    flight = Flight(
        **generate_flight_in_the_future(hours=5),
        created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


# Tokens
@pytest.fixture(scope='function')
def valid_admin_user_token(saved_valid_admin_user_model_one):
    return add_token_to_response({
        'username':
        saved_valid_admin_user_model_one.username,
        'id':
        str(saved_valid_admin_user_model_one.id),
        'email':
        saved_valid_admin_user_model_one.email,
    })['token'].decode('ascii')


@pytest.fixture(scope='function')
def valid_user_one_token(saved_valid_user_one):
    return add_token_to_response({
        'username': saved_valid_user_one.username,
        'id': str(saved_valid_user_one.id),
        'email': saved_valid_user_one.email,
    })['token'].decode('ascii')
