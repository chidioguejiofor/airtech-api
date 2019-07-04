from rest_framework import serializers
from .models import Flight
from ..utils.helpers.json_helpers import raise_error
from ..utils.error_messages import serialization_errors
from django.utils import timezone
from datetime import timedelta


class FlightSerializer(serializers.ModelSerializer):
    capacity = serializers.IntegerField(min_value=1)
    type = serializers.CharField()
    currentPrice = serializers.IntegerField(source='current_price')
    createdAt = serializers.DateTimeField(source='created_at', required=False)
    updatedAt = serializers.DateTimeField(source='updated_at', required=False)

    class Meta:
        model = Flight
        fields = ('id', 'capacity', 'location', 'destination', 'schedule',
                  'currentPrice', 'type', 'created_by', 'createdAt',
                  'updatedAt')
        extra_kwargs = {
            'created_by': {
                'write_only': True
            },
        }

    def validate_type(self, validated_data):
        """Validates the flight type

        Checks if the flight type is international or local

        Args:
            validated_data(object): the data of the flight

        Returns:
            (object): the validated_data if the type is valid

        Raises:
            (ValidationError): when the type is not valid
        """
        valid_types = ('international', 'local')
        if validated_data in valid_types:
            return validated_data

        raise_error(serialization_errors['invalid_flight_type'],
                    raise_only_message=True)

    @staticmethod
    def validate_schedule(validated_data):

        if validated_data < timezone.now() - timedelta(hours=6):
            raise_error(serialization_errors['invalid_flight_schedule'],
                        raise_only_message=True)
        return validated_data

    def create(self, validated_data):
        return Flight.objects.create(**validated_data)
