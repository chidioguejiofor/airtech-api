import pytest
from airtech_api.users.models import User
from airtech_api.flight.models import Flight
from airtech_api.booking.models import Booking
from airtech_api.utils.helpers.json_helpers import add_token_to_response, generate_token
from tests.mocks.users import valid_admin_user, valid_user_one
from tests.mocks.flight import (
    valid_flight_one,
    generate_flight_with_timedelta_args,
)
from django.utils import timezone
from tests.mocks.booking import (generate_booking_model_data_with_timedelta)
from datetime import datetime, timedelta
from airtech_api.utils.constants import CONFIRM_EMAIL_TYPE, TEST_HOST_NAME
from tempfile import TemporaryFile
import os


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

    flight = Flight(**valid_flight_one,
                    created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


@pytest.fixture(scope='function')
def saved_expired_flight_one(transactional_db,
                             saved_valid_admin_user_model_one):
    flight = Flight(**generate_flight_with_timedelta_args(days=-1),
                    created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


@pytest.fixture(scope='function')
def saved_bulk_inserted_flights(transactional_db,
                                saved_valid_admin_user_model_one):
    flights = []
    for _ in range(15):
        flights.append(
            Flight(**generate_flight_with_timedelta_args(days=-1),
                   created_by=saved_valid_admin_user_model_one))

    saved_flights = Flight.objects.bulk_create(flights)
    return saved_flights


@pytest.fixture(scope='function')
def expired_booking(transactional_db, saved_valid_user_one,
                    saved_flight_with_days_to_flight_gt_60):
    booking = Booking(
        **generate_booking_model_data_with_timedelta(
            saved_valid_user_one,
            paid=False,
            flight_model=saved_flight_with_days_to_flight_gt_60),
        expiry_date=timezone.now() - timedelta(days=10),
    )
    booking.save()
    return booking


@pytest.fixture(scope='function')
def saved_bulk_inserted_bookings_for_user_one(transactional_db,
                                              saved_bulk_inserted_flights,
                                              saved_valid_user_one):
    bookings = []
    for flight in saved_bulk_inserted_flights:
        bookings.append(
            Booking(**generate_booking_model_data_with_timedelta(
                saved_valid_user_one, flight)))

    saved_bookings = Booking.objects.bulk_create(bookings)
    return saved_bookings


@pytest.fixture(scope='function')
def saved_flight_with_days_to_flight_gt_60(transactional_db,
                                           saved_valid_admin_user_model_one):
    flight = Flight(**generate_flight_with_timedelta_args(days=79),
                    created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


@pytest.fixture(scope='function')
def saved_flight_with_days_to_flight_btw_30_and_59(
        transactional_db, saved_valid_admin_user_model_one):
    flight = Flight(**generate_flight_with_timedelta_args(days=40),
                    created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


@pytest.fixture(scope='function')
def saved_flight_with_days_to_flight_btw_7_and_29(
        transactional_db, saved_valid_admin_user_model_one):
    flight = Flight(**generate_flight_with_timedelta_args(days=19),
                    created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


@pytest.fixture(scope='function')
def saved_flight_with_days_to_flight_btw_4_and_6(
        transactional_db, saved_valid_admin_user_model_one):
    flight = Flight(**generate_flight_with_timedelta_args(days=5),
                    created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


@pytest.fixture(scope='function')
def saved_flight_with_days_to_flight_btw_2_and_3(
        transactional_db, saved_valid_admin_user_model_one):
    flight = Flight(**generate_flight_with_timedelta_args(days=2.5),
                    created_by=saved_valid_admin_user_model_one)
    flight.save()
    return flight


@pytest.fixture(scope='function')
def saved_flight_with_hours_to_flight_btw_1_and_6(
        transactional_db, saved_valid_admin_user_model_one):
    flight = Flight(**generate_flight_with_timedelta_args(hours=5),
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
    })['token']


@pytest.fixture(scope='function')
def valid_user_one_token(saved_valid_user_one):
    return add_token_to_response({
        'username': saved_valid_user_one.username,
        'id': str(saved_valid_user_one.id),
        'email': saved_valid_user_one.email,
    })['token']


@pytest.fixture(scope='function')
def valid_user_one_confirm_account_token(saved_valid_user_one):
    token_data = {
        'email': saved_valid_user_one.email,
        'type': CONFIRM_EMAIL_TYPE,
        'redirect_url': 'http://{}/login'.format(TEST_HOST_NAME),
        'exp': datetime.utcnow() + timedelta(minutes=5)
    }
    return generate_token(token_data)


@pytest.fixture(scope='function')
def invalid_confirm_account_token(saved_valid_user_one):
    token_data = {
        'redirect_url': 'http://{}/login'.format(TEST_HOST_NAME),
        'exp': datetime.utcnow() + timedelta(minutes=5)
    }
    return generate_token(token_data)


@pytest.fixture(scope='function')
def expired_user_one_confirm_account_token(saved_valid_user_one):
    token_data = {
        'email': saved_valid_user_one.email,
        'type': CONFIRM_EMAIL_TYPE,
        'redirect_url': 'http://{}/login'.format(TEST_HOST_NAME),
        'exp': datetime.utcnow() - timedelta(minutes=5)
    }
    return generate_token(token_data)


@pytest.fixture(scope='function')
def non_existing_user_confirm_account_token(saved_valid_user_one):
    token_data = {
        'email': 'non-existing@email.com',
        'type': CONFIRM_EMAIL_TYPE,
        'redirect_url': 'http://{}/login'.format(TEST_HOST_NAME),
        'exp': datetime.utcnow() + timedelta(minutes=5)
    }
    return generate_token(token_data)


@pytest.fixture(scope='function')
def expired_token_for_user_one(saved_valid_user_one):
    exp_time = datetime.utcnow() - timedelta(seconds=1)
    return add_token_to_response(
        {
            'username': saved_valid_user_one.username,
            'id': str(saved_valid_user_one.id),
            'email': saved_valid_user_one.email,
        },
        exp=exp_time)['token']


@pytest.fixture(scope="session")
def low_resolution_image_file():
    filename = os.path.dirname(__file__) + '/mocks/test_image.jpg'
    with TemporaryFile() as picture:
        with open(filename, 'rb') as jpg:
            for item in jpg:
                picture.write(item)

        picture.seek(0)
        yield picture


@pytest.fixture(scope="session")
def high_resolution_image_file():
    filename = os.path.dirname(__file__) + '/mocks/high resolution image.png'
    with TemporaryFile() as picture:
        with open(filename, 'rb') as jpg:
            for item in jpg:
                picture.write(item)

        picture.seek(0)
        yield picture
