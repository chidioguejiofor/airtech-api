from django.db import models
from uuid import uuid4
from rest_framework.status import HTTP_404_NOT_FOUND
from django.utils import timezone
from django.core.exceptions import ValidationError
from ..utils.error_messages import serialization_errors
from ..utils.helpers.json_helpers import raise_error


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    @classmethod
    def get_model_or_404(cls, id, extra_filters={}, **kwargs):
        try:
            model_instance = cls.objects.filter(id=id, **extra_filters).first()
            if not model_instance:
                raise ValidationError('')
        except ValidationError:
            raise_error(
                serialization_errors['resource_id_not_found'].format(
                    cls.__name__), HTTP_404_NOT_FOUND, **kwargs)

        return model_instance
