from django.db import models
from .base_model import BaseModel
from ..users.models import User


class AuditableBaseModel(BaseModel):
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name='creator',
                                   null=True,
                                   db_column='created_by')
    updated_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name='updater',
                                   null=True,
                                   db_column='updated_by')

    class Meta:
        abstract = True
