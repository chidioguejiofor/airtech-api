from django.urls import path, re_path
from django.conf.urls import url
from .index import views as root_index
from .users.views import SignupView, LoginView, ConfirmView, resend_email
from .flight.views import FlightView, SingleFlightView
from .booking.views import BookingView, UserBookings

urlpatterns = [
    path(r'api/v1/auth/register', SignupView.as_view()),
    path(r'api/v1/auth/login', LoginView.as_view()),
    path('api/v1/flights', FlightView.as_view()),
    path('api/v1/flights/<str:id>', SingleFlightView.as_view()),
    path('api/v1/flights/<str:flight_id>/bookings', BookingView.as_view()),
    path('api/v1/user/bookings', UserBookings.as_view()),
    path('api/v1/auth/confirm-email/<str:token>', ConfirmView.as_view()),
    path('api/v1/auth/resend-email', resend_email),
    url(r'api', root_index.welcome_message),
    re_path(r'.*', root_index.catch_all),
]
