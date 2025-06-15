from django.db import models
import uuid

# Create your models here.


class DispatchRider(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    rider_name = models.CharField()
