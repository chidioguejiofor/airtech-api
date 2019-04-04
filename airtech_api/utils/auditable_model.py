from django.db import models
from .base_model import BaseModel
from ..users.models import User


class AuditableBaseModel(BaseModel):

    createdBy = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='creator',
        null=True,
        db_column='createdBy')
    updatedBy = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='updater',
        null=True,
        db_column='updatedBy')

    class Meta:
        abstract = True
