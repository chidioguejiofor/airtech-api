from rest_framework import serializers
from rest_framework.status import HTTP_404_NOT_FOUND
from ..utils.helpers.serializer_helpers import get_unique_validator
from .models import User
from ..utils.helpers.json_helpers import raise_error
from ..utils.error_messages import serialization_errors
from ..utils import custom_serializers


class LoginSerializer(serializers.Serializer):
    usernameOrEmail = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email_or_name = data['usernameOrEmail']
        if email_or_name.count('@') >= 1:
            user = User.objects.filter(email=email_or_name).first()
        else:
            user = User.objects.filter(username=email_or_name).first()

        if user and user.verify_password(data['password']):
            return user
        raise_error(serialization_errors['user_not_found'],
                    status_code=HTTP_404_NOT_FOUND,
                    raise_only_message=True)


class UserSerializer(serializers.ModelSerializer):
    firstName = custom_serializers.Alphanumeric(source='first_name',
                                                required=True)
    lastName = custom_serializers.Alphanumeric(source='last_name',
                                               required=True)
    password = serializers.CharField(write_only=True)
    gender = serializers.CharField()
    username = custom_serializers.Alphanumeric(validators=[
        get_unique_validator(User, 'username'),
    ])
    imageUrl = serializers.URLField(source='image_url', required=False)
    email = serializers.EmailField(validators=[
        get_unique_validator(User, 'email'),
    ])
    verified = serializers.BooleanField(read_only=True)
    admin = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'firstName', 'gender', 'lastName', 'email', 'username',
                  'password', 'verified', 'imageUrl', 'admin')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_gender(self, validated_data):
        gender_str = validated_data.lower()
        if gender_str in ['male', 'm']:
            return 'Male'
        elif gender_str in ['female', 'f']:
            return 'Female'

        raise raise_error(serialization_errors['invalid_gender'],
                          raise_only_message=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)
