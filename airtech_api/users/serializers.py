from rest_framework import serializers
from ..utils.helpers.serializer_helpers import get_unique_validator
from .models import User
from ..utils.helpers.json_helpers import raise_error
from ..utils.error_messages import serialization_errors


class UserSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name', required=True)
    lastName = serializers.CharField(source='last_name', required=True)
    password = serializers.CharField()
    gender = serializers.CharField()
    username = serializers.CharField(validators=[
        get_unique_validator(User, 'username'),
    ])
    email = serializers.EmailField(validators=[
        get_unique_validator(User, 'email'),
    ])

    # gender = EnumChoiceField(enum_class=GenderEnum)

    class Meta:
        model = User
        fields = ('id', 'firstName', 'gender', 'lastName', 'email', 'username',
                  'createdAt', 'updatedAt', 'password')

    def validate_gender(self, validated_data):
        gender_str = validated_data.lower()
        if gender_str in ['male', 'm']:
            return 'Male'
        elif gender_str in ['female', 'f']:
            return 'Female'

        raise raise_error(serialization_errors['invalid_gender'])

    def create(self, validated_data):
        return User.objects.create(**validated_data)
