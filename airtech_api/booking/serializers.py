from rest_framework import serializers
from .models import Booking
from ..users.serializers import UserSerializer
from ..flight.serializers import FlightSerializer
from rest_framework.validators import UniqueTogetherValidator
from ..utils.error_messages import serialization_errors
from ..utils.helpers.json_helpers import raise_error
from django.utils import timezone


class BookingSerializer(serializers.ModelSerializer):
    bookedBy = UserSerializer(source='created_by', read_only=True)
    flight = FlightSerializer(source='flight_model', required=False)
    ticketPrice = serializers.DecimalField(source='ticket_price',
                                           decimal_places=2,
                                           max_digits=100,
                                           read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', required=False)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    expiryDate = serializers.DateTimeField(source='expiry_date',
                                           read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'ticketPrice', 'flight_model', 'flight', 'bookedBy',
                  'createdAt', 'created_by', 'updatedAt', 'ticket_price',
                  'ticketPrice', 'expiryDate', 'paid')

        extra_kwargs = {
            'ticket_price': {
                'write_only': True
            },
            'flight_model': {
                'write_only': True
            },
            'created_by': {
                'write_only': True
            },
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Booking.objects.all(),
                message=serialization_errors['user_book_flight_twice'],
                fields=('flight_model', 'created_by'))
        ]

    @staticmethod
    def validate_flight_model(validated_data):

        flight_has_expired = validated_data.schedule < timezone.now()
        if flight_has_expired:
            raise_error(serialization_errors['flight_schedule_expired'],
                        raise_only_message=True)

        return validated_data

    def create(self, validated_data):
        return Booking.objects.create(**validated_data)
