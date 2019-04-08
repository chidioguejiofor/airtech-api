from airtech_api.users.models import User
from django.db.utils import IntegrityError

import pytest

from tests.mocks.users import valid_user_one, valid_user_two


@pytest.mark.django_db
class TestUserModel:
    def test_save_user_to_db_succeeds(self):
        model = User(**valid_user_one)
        model.save()
        assert valid_user_one['username'] == model.username
        assert valid_user_one['first_name'] == model.first_name
        assert valid_user_one['last_name'] == model.last_name
        assert valid_user_one['gender'] == model.gender
        assert valid_user_one['username'] == model.username

    def test_save_existing_user_fails(self):
        model = User(**valid_user_two)
        model.save()  # saves the user to db
        model = User(**valid_user_two)

        with pytest.raises(IntegrityError):
            model.save()  # should fail here
