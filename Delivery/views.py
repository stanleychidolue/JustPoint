from django import dispatch
from django.http import HttpResponseForbidden
from django.shortcuts import render
from Cart.models import Cart
from Delivery.models import DispatchRider

# Create your views here.


def show_order_details(request, order_id):
    order = Cart.objects.get(id=order_id, paid=True)
    # riders = DispatchRider.objects.filter(dispatch_type="")
    try:
        rider = DispatchRider.objects.get(email=request.user.email)
    except:
        return HttpResponseForbidden()
    if order.dispatch_rider == None:
        order.dispatch_rider = rider
        order.save()
    print(order.dispatch_rider, rider)
    if order.dispatch_rider == rider:
        return render(request, "delivery/order-details.html", {"order": order, "rider_type": rider.dispatch_type})
    else:
        return render(request, "delivery/delivery-already-accepted.html")
