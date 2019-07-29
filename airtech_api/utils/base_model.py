from django.db import models
from uuid import uuid4
from rest_framework.status import HTTP_404_NOT_FOUND
from django.utils import timezone
from django.core.exceptions import ValidationError
from ..utils.error_messages import serialization_errors


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    @classmethod
    def get_model_by_fields_or_404(cls, message_dict=None, **kwargs):
        from ..utils.helpers.json_helpers import raise_error
        message_dict = message_dict if message_dict else {}
        try:
            model_instance = cls.objects.get(**kwargs)
        except Exception:
            raise_error(
                serialization_errors['resource_id_not_found'].format(
                    cls.__name__), HTTP_404_NOT_FOUND, **message_dict)

        return model_instance

    @classmethod
    def get_model_by_id_or_404(cls, id, extra_filters={}, **kwargs):
        return cls.get_model_by_fields_or_404(id=id,
                                              message_dict=kwargs,
                                              **extra_filters)
