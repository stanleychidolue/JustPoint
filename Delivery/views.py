from django.shortcuts import render
from Cart.models import Cart

# Create your views here.


def show_order_details(request, order_id):
    order = Cart.objects.get(id=order_id)
    # if
    return render(request, "delivery/order-details.html", {"order": order})
