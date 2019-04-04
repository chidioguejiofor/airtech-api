import pytest
from airtech_api.users.models import User
from airtech_api.utils.helpers.json_helpers import add_token_to_response


@pytest.fixture(scope='module')
def valid_user_one():
    return {
        "username": "newUser",
        "first_name": "Fred",
        "last_name": "fdajhfio",
        "email": "chid101@email.com",
        "gender": "female",
        "password": "password"
    }


@pytest.fixture(scope='module')
def valid_user_two():
    return {
        "username": "newUserTwo",
        "first_name": "Fred",
        "last_name": "John",
        "email": "chid102@email.com",
        "gender": "female",
        "password": "password"
    }


@pytest.fixture(scope='module')
def valid_user_three():
    return {
        "username": "newUserThree",
        "first_name": "Fred",
        "last_name": "John",
        "email": "chid1112@email.com",
        "gender": "male",
        "password": "password"
    }


@pytest.fixture(scope='module')
def valid_flight_one():
    return {
        "capacity": 70,
        "location": "Popo York",
        "destination": "Lagos, Nigeria",
        "schedule": "2017-10-10 14:00:01",
        "amount": 4000.70,
        "type": "international"
    }


@pytest.fixture(scope='function')
def saved_valid_user_one(transactional_db, valid_user_one):

    user = User(**valid_user_one)
    user.save()
    return user


@pytest.fixture(scope='function')
def saved_valid_admin_user_model_one(transactional_db):

    user = User(
        **{
            "username": "adminUserOne",
            "first_name": "Fred",
            "last_name": "John",
            "email": "admin@email.com",
            "gender": "male",
            "password": "password",
            "admin": True
        })
    user.save()
    return user


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
def valid_user_one_token(saved_valid_user_one, valid_user_one):
    return add_token_to_response({
        'username': saved_valid_user_one.username,
        'id': str(saved_valid_user_one.id),
        'email': saved_valid_user_one.email,
    })['token'].decode('ascii')
