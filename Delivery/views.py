from django import dispatch
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render
from Cart.models import Cart
from Delivery.models import DispatchRider
import User
from User.models import CustomUser

# Create your views here.


def show_order_details(request, order_id):
    print('show_order_details')
    order = Cart.objects.get(id=order_id, paid=True)
    # riders = DispatchRider.objects.filter(dispatch_type="")
    try:
        rider = DispatchRider.objects.get(email=request.user.email)
    except:
        print('forbidden')
        return HttpResponseForbidden()
    for prod_type in order.product_type.all():
        print(prod_type.product_type, rider.dispatch_type)
        if prod_type.product_type == rider.dispatch_type:
            if prod_type.dispatch_rider == None:
                prod_type.dispatch_rider = rider
                prod_type.save()
            print(prod_type.dispatch_rider, rider)
            print(prod_type.product_type, rider.dispatch_type)
            if prod_type.dispatch_rider == rider:
                all_items = []
                total_amount, total_qty = 0, 0
                for item in order.cartitems.all():
                    if item.product and rider.dispatch_type == "Estate":
                        all_items.append(item)
                        total_amount += int(item.product.price)
                        total_qty += item.quantity
                    elif item.home_appliance and rider.dispatch_type == "HomeAppliance":
                        all_items.append(item)
                        total_amount += int(item.home_appliance.price)
                        total_qty += item.quantity

                print(total_amount, total_qty)
                customer = CustomUser.objects.get(id=order.user.id)
                context = {"order_id": order.id, "order": all_items, "total_amount": total_amount, "total_qty": total_qty,
                           "customer_name": f"{customer.first_name} {customer.last_name}", "customer_phone": customer.phone_no,
                           "delivery_address": order.delivery_address}
                return render(request, "delivery/order-details.html", context)
            else:
                return render(request, "delivery/delivery-already-accepted.html")


def delivery_completed(request, order_id):
    order = Cart.objects.get(id=order_id, paid=True)
    try:
        rider = DispatchRider.objects.get(email=request.user.email)
    except:
        return HttpResponseForbidden()
    for prod_type in order.product_type.all():
        print(prod_type.dispatch_rider, rider)
        if prod_type.dispatch_rider == rider:
            prod_type.delivered = True
            prod_type.save()
            count = 0
            for typ in order.product_type.all():
                if typ.delivered:
                    count += 1
            if count == len(order.product_type.all()):
                order.delivery_completed = True
                order.save()
            return render(request, "delivery/delivery-completed.html")
    else:
        return HttpResponseForbidden()
