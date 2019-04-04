from django.urls import path, re_path
from django.conf.urls import url
from .index import views as root_index
from .users.views import SignupView, LoginView
from .flight.views import FlightView

urlpatterns = [
    path(r'api/v1/signup', SignupView.as_view()),
    path(r'api/v1/login', LoginView.as_view()),
    path(r'api/v1/flight', FlightView.as_view()),
    url(r'api', root_index.welcome_message),
    re_path(r'.*', root_index.catch_all),
]

# urlpatterns = router.urls
