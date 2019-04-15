from django.utils import timezone
from datetime import timedelta

valid_flight_one = {
    "capacity": 70,
    "location": "Popo York",
    "destination": "Lagos, Nigeria",
    "schedule": timezone.now() + timedelta(days=30),
    "current_price": 4000.70,
    "type": "international"
}

camelized_valid_flight_one = dict(**valid_flight_one)
camelized_valid_flight_one.pop('current_price', None)
camelized_valid_flight_one['currentPrice'] = valid_flight_one.get(
    'current_price')


def generate_flight_with_timedelta_args(**timedelta_args):
    return {
        "capacity": 70,
        "location": "Popo York",
        "destination": "Lagos, Nigeria",
        "schedule": timezone.now() + timedelta(**timedelta_args),
        "current_price": 4000.70,
        "type": "international"
    }
