from django.utils import timezone
from datetime import timedelta

valid_flight_one = {
    "capacity": 70,
    "location": "Popo York",
    "destination": "Lagos, Nigeria",
    "schedule": timezone.now() + timedelta(days=30),
    "currentPrice": 4000.70,
    "type": "international"
}


def generate_flight_with_timedelta_args(**timedelta_args):
    return {
        "capacity": 70,
        "location": "Popo York",
        "destination": "Lagos, Nigeria",
        "schedule": timezone.now() + timedelta(**timedelta_args),
        "currentPrice": 4000.70,
        "type": "international"
    }
