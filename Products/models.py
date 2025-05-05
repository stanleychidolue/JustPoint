from django.db import models
from Estates.models import Shop

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=300)
    price = models.CharField(max_length=200)
    product_img = models.FileField(
        upload_to=f"images/product", default="product-default.jpg")

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.name
