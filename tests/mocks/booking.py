from django.utils import timezone
from datetime import timedelta


def generate_booking_model_data_with_timedelta(user_model,
                                               flight_model,
                                               paid=False):
    return {
        "flight_model": flight_model,
        "ticket_price": flight_model.current_price,
        "created_by": user_model,
        "paid_at": paid if paid else None,
    }
