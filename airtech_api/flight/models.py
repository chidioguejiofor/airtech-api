from airtech_api.utils.auditable_model import AuditableBaseModel
from django.db import models


# Create your models here.
class Flight(AuditableBaseModel):

    capacity = models.IntegerField(null=False)
    location = models.TextField(null=False)
    destination = models.TextField(null=False)
    schedule = models.DateTimeField(null=False)
    current_price = models.IntegerField()

    type = models.CharField(
        choices=(('local', 'local'), ('international', 'international')),
        max_length=13,
    )

    class Meta:
        db_table = 'Flight'
