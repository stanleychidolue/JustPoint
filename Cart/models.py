from django.db import models
# from Product.models import Products
from User.models import CustomUser
from Products.models import Product
from Estates.models import Shop
# from Store.templatetags.custom_tag import get_currency
# import uuid

# # Create your models here.


# class Cart(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True)
#     user = models.ForeignKey(
#         CustomUser, on_delete=models.CASCADE, null=True, blank=True)
#     session_id = models.CharField(max_length=150, null=True, blank=True)
#     paid = models.BooleanField(default=False)
#     date = models.DateField(auto_now=True)
#     transaction_id = models.CharField(max_length=200, blank=True, null=True)
#     tx_ref = models.CharField(max_length=200, blank=True, null=True)

#     def __str__(self) -> str:
#         return str(self.id)

#     @property
#     def num_of_item(self):
#         cart_items = self.cartitems.all()
#         output = sum([item.quantity for item in cart_items])
#         return output

#     @property
#     def total_cart_sum(self):
#         cart_items = self.cartitems.all()
#         total_sum = sum([item.total_item_price for item in cart_items])
#         return [total_sum, get_currency(total_sum)]

#     @property
#     def total_cart_sum_discount(self):
#         discount = 0.05*self.total_cart_sum[0]
#         return [discount, get_currency(discount)]

#     @property
#     def total_cart_sum_shipping_fee(self):
#         shipping = 0.08*self.total_cart_sum[0]
#         return [shipping, get_currency(shipping)]

#     @property
#     def total_checkout_cost(self):
#         total_checkout = self.total_cart_sum[0] + \
#             self.total_cart_sum_shipping_fee[0] - \
#             self.total_cart_sum_discount[0]
#         return [total_checkout, get_currency(total_checkout)]

#     @property
#     def product_names(self):
#         cart_items = self.cartitems.all()
#         prod_names = []
#         for item in cart_items:
#             prod_names.append(item.product.product_name)
#         return prod_names


# class CartItems(models.Model):
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)
#     cart = models.ForeignKey(
#         Cart, on_delete=models.CASCADE, related_name='cartitems')
#     quantity = models.PositiveIntegerField(default=0)
#     size = models.CharField(max_length=10, default="MD")

#     def __str__(self) -> str:
#         return self.product.product_name

#     @property
#     def total_item_price(self):
#         product_price = self.product.product_price.replace(",", "")
#         return self.quantity*int(product_price)


class FavouriteProducts(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.product


class FavouriteEstateShops(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.shop
