# Third Party Libraries
import pytest
from tempfile import NamedTemporaryFile
from airtech_api.utils.error_messages import serialization_errors
from airtech_api.users.models import User
from tests.helpers.assertion_helpers import assert_token_is_invalid, assert_expired_token
import cloudinary.uploader
from airtech_api.services.cloudinary import upload_profile_picture

from unittest.mock import Mock
from django.core.files.images import ImageFile
from rest_framework.test import APIClient
from PIL import Image
import os
django_client = APIClient()
PROFILE_PICTURE_ENDPOINT = '/api/v1/user/profile/picture'


@pytest.mark.django_db
class TestUpdateProfilePictureEndpoint:
    """
    Tests the user profile endpoints
    """

    def test_update_profile_picture_with_missing_picture_fails(
            self, client, saved_valid_user_one, valid_user_one_token):
        """SShould fail when the picture is missing in the request

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one (model): a model that represents a user in the db
            valid_user_one_token(str): a string that contains the user token
        """

        response = client.patch(
            PROFILE_PICTURE_ENDPOINT,
            # content_type='application/x-www-form-urlencoded',
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_data = response.data
        assert response.status_code == 400
        assert response_data['status'] == 'error'
        assert response_data['message'] == serialization_errors[
            'many_invalid_fields']
        assert response_data['errors']['picture'] == serialization_errors[
            'missing_field']

    def test_update_profile_picture_with_invalid_data_type_for_picture_fails(
            self, client, saved_valid_user_one, valid_user_one_token):
        """SShould fail when the picture is missing in the request

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one (model): a model that represents a user in the db
            valid_user_one_token(str): a string that contains the user token
        """

        response = django_client.patch(
            PROFILE_PICTURE_ENDPOINT,
            {'picture': 'hello_world'},
            format="multipart",
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_data = response.data
        assert response.status_code == 400
        assert response_data['status'] == 'error'
        assert response_data['message'] == serialization_errors[
            'many_invalid_fields']
        assert response_data['errors']['picture'] == serialization_errors[
            'value_not_a_file']

    def test_update_profile_picture_throws_error_does_not_break_code_succeeds(
            self, client, saved_valid_user_one, valid_user_one_token):
        """Should fail when the picture is missing in the request

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one (model): a model that represents a user in the db
            valid_user_one_token(str): a string that contains the user token
        """

        upload_profile_picture.delay = Mock(side_effect=upload_profile_picture)
        cloudinary.uploader.upload = Mock(side_effect=Exception())
        cloudinary.uploader.destroy = Mock(side_effect=lambda *args: None)

        filename = os.path.dirname(__file__) + '/mocks/test_image.jpg'
        image = Image.open(filename)

        picture = NamedTemporaryFile()
        image.save(picture, format="JPEG")

        picture.seek(0)

        response = django_client.patch(
            PROFILE_PICTURE_ENDPOINT,
            {'picture': picture},
            format="multipart",
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_data = response.data
        user = User.objects.filter(id=str(saved_valid_user_one.id)).first()
        user_id, prev_public_key, _ = upload_profile_picture.delay.call_args[0]
        assert response.status_code == 202
        assert response_data['status'] == 'success'

        assert cloudinary.uploader.upload.called
        assert upload_profile_picture.delay.called
        assert not cloudinary.uploader.destroy.called

        assert user.image_public_id is None
        assert user.image_url is None

    def test_update_profile_picture_with_large_file_fails(
            self, client, saved_valid_user_one, valid_user_one_token):
        """Should fail when the picture is missing in the request

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one (model): a model that represents a user in the db
            valid_user_one_token(str): a string that contains the user token
        """
        cloudinary_return = {
            'public_id': 'public-id',
            'secure_url': 'http://hello.com/here',
        }
        upload_profile_picture.delay = Mock(side_effect=upload_profile_picture)
        cloudinary.uploader.upload = Mock(
            side_effect=lambda *args: cloudinary_return)
        cloudinary.uploader.destroy = Mock(side_effect=lambda *args: None)

        filename = os.path.dirname(
            __file__) + '/mocks/high resolution image.png'
        image = Image.open(filename)

        picture = NamedTemporaryFile()
        image.save(picture, format="PNG")

        picture.seek(0)

        response = django_client.patch(
            PROFILE_PICTURE_ENDPOINT,
            {'picture': picture},
            format="multipart",
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_data = response.data
        assert response.status_code == 400
        assert response_data['status'] == 'error'
        assert response_data['message'] == serialization_errors[
            'image_too_large']

    def test_update_profile_picture_with_a_valid_image_succeeds(
            self, client, saved_valid_user_one, valid_user_one_token):
        """Should fail when the picture is missing in the request

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one (model): a model that represents a user in the db
            valid_user_one_token(str): a string that contains the user token
        """

        upload_profile_picture.delay = Mock(side_effect=upload_profile_picture)
        cloudinary_return = {
            'public_id': 'public-id',
            'secure_url': 'http://hello.com/here',
        }
        cloudinary.uploader.upload = Mock(
            side_effect=lambda *args: cloudinary_return)
        cloudinary.uploader.destroy = Mock(side_effect=lambda *args: None)

        filename = os.path.dirname(__file__) + '/mocks/test_image.jpg'
        image = Image.open(filename)

        picture = NamedTemporaryFile()
        image.save(picture, format="JPEG")

        picture.seek(0)

        response = django_client.patch(
            PROFILE_PICTURE_ENDPOINT,
            {'picture': picture},
            format="multipart",
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_data = response.data
        user = User.objects.filter(id=str(saved_valid_user_one.id)).first()
        user_id, prev_public_key, _ = upload_profile_picture.delay.call_args[0]
        assert response.status_code == 202
        assert response_data['status'] == 'success'

        assert cloudinary.uploader.upload.called
        assert upload_profile_picture.delay.called
        assert not cloudinary.uploader.destroy.called

        assert prev_public_key is None
        assert user_id == saved_valid_user_one.id

        assert user.image_public_id == cloudinary_return['public_id']
        assert user.image_url == cloudinary_return['secure_url']

    def test_delete_existing_cloudinary_image_if_user_had_one_succeeds(
            self, client, saved_valid_user_one, valid_user_one_token):
        """Should fail when the picture is missing in the request

        Args:
            client (fixture): a fixture used to make HTTP request
            saved_valid_user_one (model): a model that represents a user in the db
            valid_user_one_token(str): a string that contains the user token
        """
        prev_image_data = {
            'image_public_id': 'random-key',
            'image_url': 'http://random-url/name'
        }
        saved_valid_user_one.image_public_id = prev_image_data[
            'image_public_id']
        saved_valid_user_one.image_url = prev_image_data['image_url']
        saved_valid_user_one.save()

        upload_profile_picture.delay = Mock(side_effect=upload_profile_picture)
        cloudinary_return = {
            'public_id': 'public-id',
            'secure_url': 'http://hello.com/here',
        }
        cloudinary.uploader.upload = Mock(
            side_effect=lambda *args: cloudinary_return)
        cloudinary.uploader.destroy = Mock(side_effect=lambda *args: None)

        filename = os.path.dirname(__file__) + '/mocks/test_image.jpg'
        image = Image.open(filename)

        picture = NamedTemporaryFile()
        image.save(picture, format="JPEG")

        picture.seek(0)

        response = django_client.patch(
            PROFILE_PICTURE_ENDPOINT,
            {'picture': picture},
            format="multipart",
            HTTP_AUTHORIZATION='Bearer {}'.format(valid_user_one_token),
        )

        response_data = response.data
        user = User.objects.filter(id=str(saved_valid_user_one.id)).first()
        user_id, prev_public_key, _ = upload_profile_picture.delay.call_args[0]
        destroy_arg = cloudinary.uploader.destroy.call_args[0][0]
        assert response.status_code == 202
        assert response_data['status'] == 'success'

        assert cloudinary.uploader.upload.called
        assert upload_profile_picture.delay.called
        assert cloudinary.uploader.destroy.called

        assert prev_public_key == prev_image_data['image_public_id']
        assert destroy_arg == prev_image_data['image_public_id']

        assert user_id == saved_valid_user_one.id

        assert user.image_public_id == cloudinary_return['public_id']
        assert user.image_url == cloudinary_return['secure_url']
