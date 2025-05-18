from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from Estates.models import Estate, Shop
from Home.models import HomeAppliances
from Products.models import Product
from Cart.models import (FavouriteEstateShops,
                         FavouriteProducts, Cart, CartItems)
from django.db.utils import IntegrityError


from .views import FavouriteEstateShops, FavouriteProducts
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

import json
import uuid
import requests
import os

# Create your views here.


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
    elif fav_type == "product":
        product = Product.objects.get(id=id)
        item = FavouriteProducts(user=request.user, product=product)

    try:
        item.save()
    except IntegrityError:
        return JsonResponse({"status_code": 400, "message": "item_already_saved"})

    response = {"status_code": 200, "message": "Saved Successfully"}
    return JsonResponse(response)


def rm_from_fav(request):
    data = json.loads(request.body)
    id = data['id']
    fav_type = data.get('favType')

    if fav_type == "estate":
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
        response = response.json()
        cart_id = response['data']['meta']['cart_id']
        cart = Cart.objects.get(id=cart_id, paid=False)
        if response['data']['status'] == "successful" and response['data']['amount'] >= cart.total_checkout_cost[0] and response['data']['currency'] == "NGN":
            transaction_id = response['data'].get("id")
            cart.paid, cart.transaction_id, cart.tx_ref = True, transaction_id, tx_ref
            cart.save()
            return render(request, 'cart/checkout-complete.html', {"order_id": cart_id})
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
            "Authorization": "Bearer " + os.environ.get("FLUTTER_API_KEY")
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
                'title': "NaestPoint Product Payment",
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

        response = response.json()
        flutter_link = response["data"]["link"]
        return HttpResponseRedirect(flutter_link)
    return redirect("cart-page")


def cart_page(request):
    return render(request, 'cart/cart.html')


def delete_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user, paid=False)
        cart_items = cart.cartitems.all()
        cart_items.delete()
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
    print(product_type)
    if product_type == "product":
        product = Product.objects.get(id=product_id)
    elif product_type == "appliance":
        product = HomeAppliances.objects.get(id=product_id)

    print(product)
    user = request.user
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user, paid=False)
        saved_items = FavouriteProducts.objects.filter(user=user)
        try:
            item = FavouriteProducts.objects.get(product=product)
        except:
            item = product
        if item in saved_items:
            item.delete()
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
        elif product_type == "appliance":
            cart_item, created = CartItems.objects.get_or_create(
                cart=cart, home_appliance=product)
        prod_available = False
        cart_item.quantity += 1
        cart_item.save()
        if product_type == "product":
            prod_pk = cart_item.product.pk
        elif product_type == "appliance":
            prod_pk = cart_item.home_appliance.pk
    response = {"num_of_cart_items": cart.num_of_item, "item_qty": cart_item.quantity,
                "total_cart_sum": cart.total_cart_sum[1], "total_cart_sum_disc": cart.total_cart_sum_discount[1],
                "total_cart_sum_shipping_fee": cart.total_cart_sum_shipping_fee[1], "total_checkout_cost": cart.total_checkout_cost[1],
                "item_prod_id": prod_pk,
                "prod_in_cart": prod_available}
    return JsonResponse(response)
    # return JsonResponse(cart.num_of_item,safe=False)


def rm_from_cart(request):
    data = json.loads(request.body)
    product_id = data['id']
    event_trigger = data.get("eventTrigger")
    product_type = data.get("product_type")
    print(product_type)
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
    elif product_type == "appliance":
        cart_item, created = CartItems.objects.get_or_create(
            cart=cart, home_appliance=product)

    if event_trigger != "button":
        cart_item.quantity -= 1
        if cart_item.quantity < 1:
            cart_item.delete()
        else:
            cart_item.save()

    if product_type == "product":
        prod_pk = cart_item.product.pk
    elif product_type == "appliance":
        prod_pk = cart_item.home_appliance.pk
    response = {"num_of_cart_items": cart.num_of_item, "item_qty": cart_item.quantity,
                "total_cart_sum": cart.total_cart_sum[1], "total_cart_sum_disc": cart.total_cart_sum_discount[1],
                "total_cart_sum_shipping_fee": cart.total_cart_sum_shipping_fee[1],
                "total_checkout_cost": cart.total_checkout_cost[1], "item_prod_id": prod_pk}
    return JsonResponse(response)
    # return JsonResponse(cart.num_of_item,safe=False)
