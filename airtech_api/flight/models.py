from airtech_api.utils.auditable_model import AuditableBaseModel
from django.db import models


# Create your models here.
class Flight(AuditableBaseModel):

    capacity = models.IntegerField(null=False)
    location = models.TextField(null=False)
    destination = models.TextField(null=False)
    schedule = models.DateTimeField(null=False)
    currentPrice = models.DecimalField(decimal_places=2, max_digits=100)

    type = models.CharField(
        choices=(('local', 'local'), ('international', 'international')),
        max_length=13,
    )

    class Meta:
        db_table = 'Flight'
