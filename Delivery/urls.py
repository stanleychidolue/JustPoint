from django.urls import path
from . import views


urlpatterns = [
    # cart functionalities urls
    path("view-order-items/<order_id>",
         views.show_order_details, name="view-order-items"),
    path("delivery-completed/<order_id>",
         views.delivery_completed, name="delivery-completed"),
]
