from rest_framework.validators import UniqueValidator
from ...utils.error_messages import serialization_errors


def get_unique_validator(model, *err_options, err_key='unique'):
    return UniqueValidator(
        queryset=model.objects.all(),
        message=serialization_errors[err_key].format(*err_options),
    )
