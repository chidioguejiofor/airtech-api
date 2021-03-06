from django.urls import path, re_path
from django.conf.urls import url
from .index import views as root_index
from .users.views import (SignupView, LoginView, ConfirmView,
                          ResendEmailEndpoint, UserProfilePicture,
                          RequestAdminAccessView, accept_admin_request)

from .flight.views import FlightView, SingleFlightView
from .booking.views import BookingView, UserBookings, UserPayment, SingleUserBookings

urlpatterns = [
    path(r'api/v1/auth/register', SignupView.as_view()),
    path(r'api/v1/auth/login', LoginView.as_view()),
    path('api/v1/auth/confirm-email/<str:token>', ConfirmView.as_view()),
    path('api/v1/auth/request-admin-access', RequestAdminAccessView.as_view()),
    path('api/v1/auth/request-admin-access/<str:token>', accept_admin_request),
    path('api/v1/auth/resend-email', ResendEmailEndpoint.as_view()),
    path('api/v1/flights', FlightView.as_view()),
    path('api/v1/flights/<str:id>', SingleFlightView.as_view()),
    path('api/v1/flights/<str:flight_id>/bookings', BookingView.as_view()),
    path('api/v1/user/bookings', UserBookings.as_view()),
    path('api/v1/user/bookings/<str:id>', SingleUserBookings.as_view()),
    path('api/v1/user/bookings/<str:id>/payment', UserPayment.as_view()),
    path('api/v1/user/profile/picture', UserProfilePicture.as_view()),
    url(r'api', root_index.welcome_message),
    re_path(r'.*', root_index.catch_all),
]
