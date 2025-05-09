from django.db import models

# Create your models here.


class Estate(models.Model):
    name = models.CharField(max_length=250,)
    state = models.CharField(max_length=100,)
    lga = models.CharField(max_length=100, name='LGA')
    district = models.CharField(max_length=150, name="district")

    def __str__(self) -> str:
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=250,)
    description = models.TextField()
    img_logo = models.FileField(
        upload_to=f"images/shop", default="shop-default.jpg", null=True)
    type = models.CharField(max_length=50, choices=(
        ('SHOP', u'SHOP'),
        ('VENDOR', u'VENDOR'),
    ))
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, default=0)

    def __str__(self) -> str:
        return self.name
