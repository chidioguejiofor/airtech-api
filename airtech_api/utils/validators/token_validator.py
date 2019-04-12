import os

from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from rest_framework.permissions import BasePermission
from ..error_messages import tokenization_errors
import jwt

# Models
from ...users.models import User
from ..helpers.json_helpers import raise_error


class TokenValidator(BasePermission):
    validation_error_message = tokenization_errors['token_is_invalid']
    validation_status_code = HTTP_401_UNAUTHORIZED

    def has_permission(self, request, view):

        # if request.method not in view.protected_methods:
        #     return True

        if 'Authorization' not in request.headers:
            raise_error(
                tokenization_errors['missing_token'],
                status_code=HTTP_401_UNAUTHORIZED)

        authorization = request.headers.get('Authorization').split(' ')

        if len(authorization) != 2 or authorization[0] != 'Bearer':
            raise_error(
                tokenization_errors['token_format_error'],
                status_code=HTTP_401_UNAUTHORIZED)

        token = authorization[1]
        data = self.decode_token(token)

        user = User.objects.filter(id=data.get('id', '')).first()

        if not self.is_user_valid(user, request, view):
            raise_error(
                self.validation_error_message,
                status_code=self.validation_status_code)

        request.decoded_user = user

        return True

    @staticmethod
    def decode_token(token):
        """Decodes a token sent by the user

        Args:
            token (str): The token sent by the user

        Raises:
           (jwt.ExpiredSignatureError): when the token has expired
           (jwt.exceptions.DecodeError): when  the token was not decoded successfully
        Returns:
            (dict): The data contained in the token
        """
        try:
            return jwt.decode(
                token, os.getenv('JWT_SCRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise_error(
                tokenization_errors['expired_token'],
                status_code=HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
            raise_error(
                tokenization_errors['token_is_invalid'],
                status_code=HTTP_401_UNAUTHORIZED)

    def is_user_valid(self, user, request, view):
        """Checks if the user is valid

        Returns True if the user is valid or False if the user is not

        Note that all subclasses of the TokenValidator must override this method to suit their needs

        Args:
            user (User): The user model to be tested
            request (Request): An object containing the user request
            view (View): The current view

        Returns:
            True when the user is object is valid or False if it is not
        """
        return user


class AdminTokenValidator(TokenValidator):
    validation_error_message = tokenization_errors['user_is_forbidden']
    validation_status_code = HTTP_403_FORBIDDEN

    def is_user_valid(self, user, request, view):
        """Checks if the user is and admin

        Note that all subclasses of the TokenValidator must override this method to suit their needs

        Args:
            user (User): The user model to be tested
            request (Request): An object containing the user request
            view (View): The current view

        Returns:
            True when the user is an admin
        """
        if request.method in view.regular_user_methods:
            return super().is_user_valid(user, request, view)
        return user and user.admin is True
