from rest_framework import serializers
from .models import Flight
from ..utils.helpers.json_helpers import raise_error
from ..utils.error_messages import serialization_errors
from ..users.serializers import UserSerializer


class FlightSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    creator = UserSerializer(source='createdBy', read_only=True)
    amount = serializers.DecimalField(decimal_places=2, max_digits=100)
    createdAt = serializers.DateTimeField(required=False)

    class Meta:
        model = Flight
        fields = ('id', 'capacity', 'location', 'destination', 'schedule',
                  'amount', 'type', 'creator', 'createdBy', 'createdAt',
                  'updatedAt')
        extra_kwargs = {'createdBy': {'write_only': True}}

    def validate_type(self, validated_data):
        valid_types = ('international', 'local')
        if validated_data in valid_types:
            return validated_data

        raise_error(
            serialization_errors['invalid_flight_type'],
            raise_only_message=True)

    def create(self, validated_data):
        return Flight.objects.create(**validated_data)
