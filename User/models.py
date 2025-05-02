from django.db import models
from django.contrib.auth.models import AbstractUser
# pip install "django-phonenumber-field[phonenumbers]"
# from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=100, null=True, blank=True, unique=True)
    email = models.EmailField(unique=True)
    # phone_no = PhoneNumberField(null=True, unique=False)
    phone_no = models.CharField(max_length=11, unique=True)
    address = models.TextField(null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
