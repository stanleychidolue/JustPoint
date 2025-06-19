from django.db import models
import uuid

# Create your models here.


class DispatchRider(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    dispatch_type = models.CharField(max_length=150, choices=(
        ('Estate', u'Estate'),
        ('Market', u'Market'),
        ('Restaurant', u'Restaurant'),
    ))
    rider_image = models.FileField(
        upload_to="images/rider_profiles", default="default_carousel.jpg")
    rider_location = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
