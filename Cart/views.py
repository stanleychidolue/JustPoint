from hashlib import file_digest
from Delivery.models import DispatchRider
from tools import send_delivery_request
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden
from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from Estates.models import Estate, Shop
from Home.models import HomeAppliances
from Products.models import Product
from Cart.models import (FavouriteEstateShops,
                         FavouriteProducts, Cart, CartItems, ProductType)
from django.db.utils import IntegrityError


from .views import FavouriteEstateShops, FavouriteProducts
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from dotenv import load_dotenv
from django.core.cache import cache

import json
import uuid
import requests
import os


# Create your views here.

load_dotenv()

CACHE_TIMEOUT = 60*10


# @login_required
def favourite(request, option):
    favourites = []
    if request.user.is_authenticated:
        if option == "estate":
            estate_fav = FavouriteEstateShops.objects.filter(user=request.user)
            favourites = [saved.shop for saved in estate_fav]

        if option == "product":
            product_fav = FavouriteProducts.objects.filter(user=request.user)
            favourites = [saved.product for saved in product_fav]
    else:
        messages.add_message(
            request, messages.WARNING, "You need to be logged in to view your favourites")
        return redirect("/user/login/?next=/customer/view-favourite/estate/")

    return render(request, "cart&fav/favourite.html", {f"{option}": True, 'favourites': favourites})


def add_to_fav(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status_code": 401, "message": "user_not_authenticated"})
    data = json.loads(request.body)
    id = data['id']
    fav_type = data.get('favType')

    if fav_type == "estate":
        shop = Shop.objects.get(id=id)
        item = FavouriteEstateShops(user=request.user, shop=shop)
        if FavouriteEstateShops.objects.filter(user=item.user, shop=item.shop).exists():
            return JsonResponse({"status_code": 400, "message": "item_already_saved"})

    elif fav_type == "product":
        product = Product.objects.get(id=id)
        item = FavouriteProducts(user=request.user, product=product)
        if FavouriteProducts.objects.filter(user=item.user, product=item.product).exists():
            return JsonResponse({"status_code": 400, "message": "item_already_saved"})

    item.save()
    response = {"status_code": 200, "message": "Saved Successfully"}
    return JsonResponse(response)


def rm_from_fav(request):
    data = json.loads(request.body)
    id = data['id']
    fav_type = data.get('favType')
    if fav_type == "estate":
        # shop = Shop.objects.get(id=id)
        item = FavouriteEstateShops.objects.get(user=request.user, shop=id)
    elif fav_type == "product":
        item = FavouriteProducts.objects.get(user=request.user, product=id)
    # shop = Shop.objects.get(user=request.user,product_id=id)
    # usr_saved_items=SavedItems.objects.filter(user=request.user)
    item.delete()
    response = {"message": "Removed Successfully"}
    return JsonResponse(response)


def checkout_complete(request):
    status = request.GET.get('status', None)
    if status == "successful":
        tx_ref = request.GET.get('tx_ref', None)
        transaction_id = request.GET["transaction_id"]
        # reconfirm/verify transaction
        # verify by transcation_id(params not required)
        url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
        # url="https://api.flutterwave.com/v3/transactions/verify_by_reference"       #verify by tx-ref(params required)

        header = {
            "Authorization": "Bearer " + os.environ.get("FLUTTER_API_KEY")
        }
        params = {"tx_ref": tx_ref}
        try:
            response = requests.get(url=url, headers=header, params=params)
        except Exception as error:
            print(f"This is the error: {error} /n response:{response}")
            messages.add_message(request, messages.WARNING,
                                 "Transaction status not verified!!! Please wait a moment.")
            return redirect('cart-page')
        if response.status_code == 200:
            response = response.json()
            cart_id = response['data']['meta']['cart_id']
            cart = Cart.objects.get(id=cart_id, paid=False)
            if response['data']['status'] == "successful" and response['data']['amount'] >= cart.total_checkout_cost[0] and response['data']['currency'] == "NGN":
                transaction_id = response['data'].get("id")
                cart.paid, cart.transaction_id, cart.tx_ref = True, transaction_id, tx_ref
                cart.save()
                return render(request, 'cart&fav/checkout-complete.html', {"order_id": cart_id})
        else:
            messages.add_message(request, messages.WARNING,
                                 "Transaction status not verified!!! Please wait a moment.")
            return redirect('cart-page')

    else:
        messages.add_message(request, messages.WARNING,
                             "Transaction Failed!!!  Your payment was not successfull")
        return redirect('cart-page')


@login_required()
def checkout(request):
    if request.method == "POST":
        total_cost = request.POST.get("total_checkout_cost")
        cart = Cart.objects.get(user=request.user, paid=False)
        redirect_url = request.build_absolute_uri(
            reverse('checkout-complete-page'))

        url = "https://api.flutterwave.com/v3/payments"
        header = {
            "accept": "application/json",
            "Authorization": "Bearer " + os.environ.get("FLUTTER_API_KEY"),
            "Content-Type": "application/json"
        }
        data = {
            "tx_ref": str(uuid.uuid4()),
            "amount": total_cost,
            "currency": "NGN",
            "redirect_url": redirect_url,
            "meta": {
                "consumer_id": request.user.pk,
                # "consumer_mac": "92a3-912ba-1192a",
                "cart_id": str(cart.id)
            },
            "customer": {
                "email": request.user.email,
                # needs to str and not Object of type PhoneNumber
                "phonenumber": str(request.user.phone_no),
                "name": request.user.first_name
            },
            "customizations": {
                'title': "JustPoint Product Payment",
                "logo": "https://nastpoints3bucket.s3.eu-north-1.amazonaws.com/static/images/NaestPoint-favicon.ico"
            },
            "configurations": {
                # Session timeout in minutes (maxValue: 1440 minutes)
                "session_duration": 10,
                "max_retry_attempt": 2,  # Max retry (int)
            },
        }

        try:
            response = requests.post(url=url, headers=header, json=data)
        except Exception as e:
            print(
                f"An error occured when fetching payment confirmation,this is the error: {e}")
            messages.add_message(
                request, messages.WARNING, "An error occured, please try again.")
            return redirect("cart-page")
        if response.status_code == 200:
            response = response.json()
            flutter_link = response["data"]["link"]
            return HttpResponseRedirect(flutter_link)
        else:
            messages.add_message(
                request, messages.WARNING, "An error occured, please try again.")
            return redirect("cart-page")
    return redirect("cart-page")


@login_required()
def payment_options(request):
    if request.method == "POST":
        total_cost = request.POST.get("total_checkout_cost")
        cart = Cart.objects.get(user=request.user, paid=False)
        if cache.has_key("transaction_id"):
            transaction_id = cache.get("transaction_id")

        else:
            transaction_id = str(
                uuid.uuid4().hex[:16])
            cache.set("transaction_id", transaction_id, 60*60*24)
            # save the generated transaction_id to the user cart
            cart.transaction_id = transaction_id
            cart.save()
        context = {"amount": int(float(total_cost)),
                   "transaction_id": transaction_id}
        return render(request, 'cart&fav/payment-options.html', context)

# @login_required()


def confirm_client_payment(request):
    if request.method == "POST":
        body = json.loads(request.body)
        transaction_id = body.get("transactionId")
        amount = body.get("amount")
        customer_name = body.get("customerName")
        # customer_name, transaction_id, amount = "stanley chidolue", "60f24855bba04c6380a007eb75081c90", 200

        cart = Cart.objects.get(transaction_id=transaction_id)
        if cart.paid == True:
            return JsonResponse({"status_code": 200, "message": "Payment Successful", "order_id": cart.id})
            # send a request to the bank alert checker API
        url = "http://127.0.0.1:8000/check-transaction"
        header = {
            "accept": "application/json",
            "Authorization": "Bearer " + os.environ.get("JUSTPOINT_API_KEY"),
            "Content-Type": "application/json"
        }
        params = {"transaction_id": transaction_id,
                  "amount": int(float(amount)),
                  "full_name": customer_name,
                  "cart_id": cart.pk

                  }
        try:
            response = requests.get(url=url, headers=header, params=params)
            print(response.text)
            if response.status_code == 200 and response.json().get("status") == "success":
                print(200)
                response = response.json()
                # response = {
                #     "data": {"transaction_id": transaction_id, "amount": int(float(amount)), }}
                data = response['data']
                trans_id, trans_amount, customer_name, cart_id = data.get("transaction_id"), data.get(
                    "transaction_amount"), data.get("customer_name"), data.get("cart_id")
                print(trans_id)
                try:
                    try:
                        cart = Cart.objects.get(
                            transaction_id=trans_id.lower(), paid=False)
                    except:
                        cart = Cart.objects.get(
                            id=cart_id, paid=False)
                    print(cart)
                    if trans_amount >= cart.total_checkout_cost[0]:
                        cart.paid, cart.transaction_id, cart.tx_ref, cart.payer_name = True, trans_id, transaction_id, customer_name
                        cart.save()
                        print("i saved the cart successfully")
                except Exception as e:
                    print("Cart is already saved as paid")
                return JsonResponse({"status_code": 200, "message": "Payment Successful", "order_id": cart.id})
            else:
                print("yes")
                # html = render_to_string(
                #     'cart&fav/payment-confirm-failed.html', {"order_id": "jhfyeg7w"})
                # return JsonResponse({'html': html})
                return JsonResponse({"status_code": 401, "message": "Payment not yet reflected, could not confirm Payment", "order_id": cart.transaction_id})
        except Exception as error:
            print(f"This is the error: {error} /n response:{error}")
            # messages.add_message(request, messages.WARNING,
            #                      "Transaction status not verified!!! Please wait a moment.")

            return JsonResponse({"status_code": 400, "message": "Could not confirm Payment", "order_id": cart.transaction_id})
    return HttpResponseForbidden()


def payment_confirm_failed(request, order_id):
    cart = Cart.objects.get(transaction_id=order_id, paid=False)
    context = {
        "amount": cart.total_checkout_cost[0], "transaction_id": cart.transaction_id}
    return render(request, 'cart&fav/payment-confirm-failed.html', context)


def payment_confirm_success(request, order_id):
    result = cache.delete("transaction_id")
    print(result)
    redirect_url = request.build_absolute_uri(
        reverse('view-order-items', kwargs={"order_id": order_id}))
    print(redirect_url)
    # redirect_url = f"http://127.0.0.1:3000/delivery/view-order-items/{order_id}"
    order = Cart.objects.get(id=order_id, paid=True)

    prod_types = {}
    for item in order.cartitems.all():
        if item.product:
            prod_types["Estate"] = item.product.shop.estate
        elif item.home_appliance:
            prod_types["Market"] = None
        print(prod_types)
    for type, location in prod_types.items():
        riders = DispatchRider.objects.filter(dispatch_type=type)
        try:
            nearby_riders = riders.filter(rider_location=location)
            if len(nearby_riders) != 0:
                riders = nearby_riders
        except:
            pass
        send_delivery_request(redirect_url, riders)
    return redirect("payment-confirmed", order_id=order_id)


def payment_confirmed(request, order_id):
    order = Cart.objects.get(id=order_id, paid=True)
    return render(request, 'cart&fav/checkout-complete.html', {"order_id": order.id, "delivery_address": order.delivery_address})


def edit_delivery_address(request, order_id):
    if request.method == "POST":
        new_delivery_address = request.POST.get("edited-address")
        order = Cart.objects.get(id=order_id, paid=True)
        order.delivery_address = new_delivery_address
        order.save()
        return redirect('payment-confirmed', order_id=order_id)
    else:
        return HttpResponseForbidden()


def cart_page(request):
    return render(request, 'cart&fav/cart.html')


def delete_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user, paid=False)
        print(cart.product_type.all())
        item_types = ProductType.objects.filter(
            cart=cart)
        cart_items = cart.cartitems.all()
        cart_items.delete()

        for item_type in item_types:
            item_type.delete()

    else:
        cart = Cart.objects.get(
            session_id=request.session.get('session_id'), paid=False)
        cart_items = cart.cartitems.all()
        cart_items.delete()
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)


def add_to_cart(request, option):
    data = json.loads(request.body)
    product_id = data['id']
    event_trigger = data.get("eventTrigger")
    product_type = data.get("product_type")
    if product_type == "product":
        product = Product.objects.get(id=product_id)
    elif product_type == "appliance":
        product = HomeAppliances.objects.get(id=product_id)
    user = request.user
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=user, paid=False, delivery_address=request.user.address)
        # saved_items = FavouriteProducts.objects.filter(user=user)
        # try:
        #     item = FavouriteProducts.objects.get(product=product)
        # except:
        #     item = product
        # if item in saved_items:
        #     item.delete()
    else:
        try:
            session = request.session['session_id']
        except:
            session = request.session['session_id'] = str(uuid.uuid4())
        cart, created = Cart.objects.get_or_create(
            session_id=session, paid=False)
    if product.name in cart.product_names and option != "increase":
        if product_type == "product":
            cart_item = CartItems.objects.get(cart=cart, product=product)
        elif product_type == "appliance":
            cart_item = CartItems.objects.get(
                cart=cart, home_appliance=product)
        prod_available = True
        if event_trigger != "button":
            cart_item.delete()
    else:
        if product_type == "product":
            cart_item, created = CartItems.objects.get_or_create(
                cart=cart, product=product)
            item_type, created = ProductType.objects.get_or_create(
                cart=cart, product_type="Estate")
        elif product_type == "appliance":
            cart_item, created = CartItems.objects.get_or_create(
                cart=cart, home_appliance=product)
            item_type, created = ProductType.objects.get_or_create(
                cart=cart, product_type="HomeAppliance")

        prod_available = False
        cart_item.quantity += 1
        cart_item.save()
        try:
            if not item_type in cart.product_type.all():
                item_type.save()
        except Exception as e:
            print(e)
    if product_type == "product":
        prod_pk = cart_item.product.pk
    elif product_type == "appliance":
        prod_pk = cart_item.home_appliance.pk
    response = {"num_of_cart_items": cart.num_of_item, "item_qty": cart_item.quantity,
                "total_cart_sum": cart.total_cart_sum[1], "total_cart_sum_disc": cart.total_cart_sum_discount[1],
                "total_cart_sum_shipping_fee": cart.total_cart_sum_shipping_fee[1], "total_checkout_cost": cart.total_checkout_cost,
                "item_prod_id": prod_pk,
                "prod_in_cart": prod_available}
    return JsonResponse(response)
    # return JsonResponse(cart.num_of_item,safe=False)


def rm_from_cart(request):
    data = json.loads(request.body)
    product_id = data['id']
    event_trigger = data.get("eventTrigger")
    product_type = data.get("product_type")
    if product_type == "product":
        product = Product.objects.get(id=product_id)
    elif product_type == "appliance":
        product = HomeAppliances.objects.get(id=product_id)
    user = request.user
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user, paid=False)

    else:
        try:
            session = request.session['session_id']
        except:
            session = request.session['session_id'] = str(uuid.uuid4())
        cart, created = Cart.objects.get_or_create(
            session_id=session, paid=False)

    if product_type == "product":
        cart_item, created = CartItems.objects.get_or_create(
            cart=cart, product=product)
        item_type = ProductType.objects.get(
            cart=cart, product_type="Estate")

    elif product_type == "appliance":
        cart_item, created = CartItems.objects.get_or_create(
            cart=cart, home_appliance=product)
        item_type = ProductType.objects.get(
            cart=cart, product_type="HomeAppliance")

    if event_trigger != "button":
        cart_item.quantity -= 1
        if cart_item.quantity < 1:
            cart_item.delete()
            prod_types_in_cart = []
            for item in cart.cartitems.all():
                if item.product:
                    prod_types_in_cart.append("Estate")
                elif item.home_appliance:
                    prod_types_in_cart.append("HomeAppliance")
            if not item_type.product_type in prod_types_in_cart:
                item_type.delete()
        else:
            cart_item.save()

    if product_type == "product":
        prod_pk = cart_item.product.pk
    elif product_type == "appliance":
        prod_pk = cart_item.home_appliance.pk
    response = {"num_of_cart_items": cart.num_of_item, "item_qty": cart_item.quantity,
                "total_cart_sum": cart.total_cart_sum[1], "total_cart_sum_disc": cart.total_cart_sum_discount[1],
                "total_cart_sum_shipping_fee": cart.total_cart_sum_shipping_fee[1],
                "total_checkout_cost": cart.total_checkout_cost, "item_prod_id": prod_pk}
    return JsonResponse(response)
    # return JsonResponse(cart.num_of_item,safe=False)
