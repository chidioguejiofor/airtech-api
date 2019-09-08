from django.utils.translation import gettext_lazy
from rest_framework.serializers import RegexField
from ..error_messages import serialization_errors


class Alphanumeric(RegexField):
    default_error_messages = {
        'invalid': gettext_lazy(serialization_errors['only_alpha_and_numbers'])
    }

    def __init__(self, *args, **kwargs):
        super().__init__('^[a-zA-Z0-9]+$', *args, **kwargs)
