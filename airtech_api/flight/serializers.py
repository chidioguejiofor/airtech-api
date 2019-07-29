from rest_framework import serializers
from .models import Flight
from ..utils.helpers.json_helpers import raise_error
from ..utils.error_messages import serialization_errors
from ..utils.helpers.serializer_helpers import UpdateableSerializer
from django.utils import timezone
from datetime import timedelta


class FlightSerializer(UpdateableSerializer):
    updateable_fields = [
        'capacity',
        'type',
        ('currentPrice', 'current_price'),
        'location',
        'destination',
    ]
    uneditable_fields = ['schedule']

    capacity = serializers.IntegerField(min_value=1)
    type = serializers.CharField()
    currentPrice = serializers.IntegerField(source='current_price')
    createdAt = serializers.DateTimeField(source='created_at', required=False)
    updatedAt = serializers.DateTimeField(source='updated_at', required=False)

    class Meta:
        model = Flight
        fields = [
            'id', 'capacity', 'location', 'destination', 'schedule',
            'currentPrice', 'type', 'created_by', 'createdAt', 'updatedAt'
        ]
        extra_kwargs = {
            'created_by': {
                'write_only': True
            },
        }

    @classmethod
    def update_data_from_requests(cls,
                                  user_request,
                                  model,
                                  fields_to_update=None):
        """Ensured that the user cannot update location and destination if flight is booked

        Args:
            user_request(dict): this contains the user request
            model(Flight): the flight model
        Raises ValidationError:
            when the the flight has bookings and the user is trying to update
            either location or destination

        """

        err_dict = cls._generate_for_errors_object_when_updating(user_request)
        if len(err_dict) > 0:
            raise_error(serialization_errors['many_invalid_fields'],
                        err_dict=err_dict)
        return super().update_data_from_requests(user_request, model,
                                                 fields_to_update)

    @staticmethod
    def _generate_for_errors_object_when_updating(user_request):
        """Generates error object when updating

        Args:
            user_request: The user request object

        Returns:
            (dict): error dictionary which can be empty or with errors
        """
        err_dict = {}
        for field in ['location', 'destination']:
            if field in user_request:
                err_dict[field] = \
                    [serialization_errors['cannot_update_flight_field_with_bookings'].format(field)]

        return err_dict

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
