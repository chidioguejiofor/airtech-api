from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.utils import timezone
from rest_framework.status import HTTP_201_CREATED
from ...utils import success_messages
from ..helpers.json_helpers import generate_response, raise_error
from ...utils.error_messages import serialization_errors


def get_unique_validator(model, *err_options, err_key='unique'):
    return UniqueValidator(
        queryset=model.objects.all(),
        message=serialization_errors[err_key].format(*err_options),
    )


class UpdateableSerializer(serializers.ModelSerializer):
    updateable_fields = []
    uneditable_fields = []

    @classmethod
    def update_data_from_requests(cls,
                                  user_request,
                                  model,
                                  fields_to_update=None):
        MODEL_NAME = model.__class__.__name__

        cls._validate_user_request(user_request, MODEL_NAME)
        serializer = cls.create_serializer_from_user_request(
            user_request, model, fields_to_update)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return generate_response(
                success_messages['update'].format(model.__class__.__name__),
                serializer.data,
                status_code=HTTP_201_CREATED,
            )
        raise_error(serialization_errors['many_invalid_fields'],
                    err_dict=serializer.errors)

    @classmethod
    def create_serializer_from_user_request(cls, user_request, model,
                                            fields_to_update):
        """Creates a serializer based on user request

        Args:
            user_request (dict): contains the user request
            model (Model): the model that contains the data
            fields_to_update: the fields that can be updated

        Returns:

        """
        data = {}
        fields_to_update = fields_to_update if fields_to_update else cls.updateable_fields
        for list_item in fields_to_update:

            if isinstance(list_item, tuple):
                field_camelized, field_snake = list_item
            else:
                field_snake = field_camelized = list_item
            data[field_camelized] = user_request.get(
                field_camelized, getattr(model, field_snake))

        data['updatedAt'] = timezone.now()
        serializer = cls(model, data=data, partial=True)
        return serializer

    @classmethod
    def _validate_user_request(cls, user_request, model_name):
        """Validates that the user_request contains update_able values

        Args:
            user_request:
            model_name:

        Raises rest_framework.ValidationErrors:
            When there is an error in the user request
        """
        if len(user_request) == 0:
            raise_error(
                serialization_errors['empty_request'].format(model_name))

        err_dict = {}
        for field in cls.uneditable_fields:
            if field in user_request:
                err_dict[field] = [
                    serialization_errors['cannot_update_field'].format(
                        model_name, field)
                ]

        if len(err_dict) > 0:
            raise_error(serialization_errors['many_invalid_fields'],
                        err_dict=err_dict)
