from airtech_api.utils.auditable_model import BaseModel
from ..flight.models import Flight
from ..users.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Booking(BaseModel):
    flight_model = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name='flight',
        null=True,
        db_column='flight_id',
    )

    ticket_price = models.DecimalField(decimal_places=2,
                                       max_digits=100,
                                       null=False)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='booked_by',
        null=False,
        db_column='created_by',
    )

    expiry_date = models.DateTimeField(default=timezone.now, null=False)
    paid = models.BooleanField(default=False)

    class Meta:
        db_table = 'Booking'
        unique_together = ('flight_model', 'created_by')

    def save(self, *args, **kwargs):
        flight_time = self.flight_model.schedule
        current_time = timezone.now()
        time_to_flight = flight_time - current_time
        self.expiry_date = current_time + timedelta(hours=6)
        if time_to_flight >= timedelta(days=60):
            self.expiry_date = flight_time - timedelta(days=20)
        elif time_to_flight >= timedelta(days=30):
            self.expiry_date = flight_time - timedelta(days=5)
        elif time_to_flight >= timedelta(days=7):
            self.expiry_date = flight_time - timedelta(hours=24)
        elif time_to_flight >= timedelta(days=4):
            self.expiry_date = current_time + timedelta(hours=24)
        elif time_to_flight >= timedelta(days=2):
            self.expiry_date = current_time + timedelta(hours=12)

        self.created_at = current_time
        super().save(*args, **kwargs)
