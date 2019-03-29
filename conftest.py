import pytest


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
