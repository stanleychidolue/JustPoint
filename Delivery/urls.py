from django.urls import path
from . import views


urlpatterns = [
    # cart functionalities urls
    path("order/view-shops/<order_id>",
         views.view_shops, name="view-shops"),
    path("order/<shop>/view-shop-items/<order_id>",
         views.view_shop_items, name="view-shop-items"),
    path("view-order-items/<order_id>",
         views.show_order_details, name="view-order-items"),
    path("delivery-completed/<order_id>",
         views.delivery_completed, name="delivery-completed"),
]
