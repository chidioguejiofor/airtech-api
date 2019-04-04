from django.db import models
from uuid import uuid4
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.createdAt = timezone.now()
        super().save(*args, **kwargs)
