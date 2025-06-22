from Cart.models import Cart, CartItems, ProductType
import imp
from django.shortcuts import render, redirect
from .models import (Advertisement, UtilityPayment,
                     HomeAppliances, NewsLetters, NewsLetterSubscribers)
from .forms import NewsLetterForm
from django.core.cache import cache
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
import requests
import uuid
import os


# Create your views here.

CACHE_TIMEOUT = 60*10


def home(request):

    all_ads = cache.get_or_set(
        "all_ads", Advertisement.objects.all(), CACHE_TIMEOUT).order_by('id')
    all_utility = cache.get_or_set(
        "all_utililty", UtilityPayment.objects.all(), CACHE_TIMEOUT).order_by('id')
    all_appliance = cache.get_or_set(
        "all_appliance", HomeAppliances.objects.all(), CACHE_TIMEOUT).order_by('name')
    context = {
        "adverts": all_ads,
        "utilities": all_utility,
        "appliances": all_appliance,
    }
    return render(request, "home/index.html", context)


def services(request, service):
    return render(request, "home/service.html")


def utility_payment(request, utility_category):
    print(utility_category)

# # Flutterwave paybills API
    url = f"https://api.flutterwave.com/v3/bills/{utility_category}/billers?country=NG"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer FLWSECK_TEST-SANDBOXDEMOKEY-X",
        "Content-Type": "application/json"
    }

# # Interswitch paybills API
    # url = f"https://qa.interswitchng.com/quicktellerservice/api/v5/services"

    # headers = {
    #     "Authorization": f"Bearer {os.environ.get('ACCESS_TOKEN')}",
    #     "TerminalId": os.environ.get("TEST_TERMINAL_ID"),
    #     "Content-Type": "application/json"
    # }

    try:
        res = requests.get(url, headers=headers)
    except:
        messages.add_message(
            request, messages.WARNING, "Bill Payment Error.\nPlease try again")
        return redirect('home-page')
    if res.status_code == 200:
        dict_result = res.json()
        categories = dict_result.get('data')
        return render(request, "home/utility-options.html", {"categories": categories})
    else:
        messages.add_message(
            request, messages.WARNING, "Bill Payment Error.\nPlease try again")
        return redirect('home-page')


def validate_customer_details(request, biller_name, biller_code):

    url = f"https://api.flutterwave.com/v3/billers/{biller_code}/items"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer FLWSECK_TEST-SANDBOXDEMOKEY-X",
        "Content-Type": "application/json"
    }

    if request.method == "POST":
        identifier = request.POST.get("identifier")
        amount = request.POST.get("amount")
        category_name = request.POST.get('category-name')
        sub_plan = request.POST.get('subscription-plan')
        sub_plan = sub_plan.split(",")
        item_code, biller_name, biller_code = sub_plan[
            0], sub_plan[1], sub_plan[2]
        if amount == None:
            amount = sub_plan[3]
        print(identifier, amount, item_code,
              biller_name, biller_code, category_name)
        url = f"https://api.flutterwave.com/v3/bill-items/{item_code}/validate?"

        param = {"customer": identifier, }
        res = requests.get(url, headers=headers, params=param)
        if res.status_code != 200:
            dict_result = res.json()
            info = dict_result.get('data')
            context = {"customer_info": info, "category_name": category_name,
                       "amount": amount, 'item_code': item_code, 'biller_name': biller_name, "biller_code": biller_code}
            return render(request, 'home/confirm-details.html', context)
        else:
            messages.add_message(
                request, messages.WARNING, "Customer's details could not be validated.\nPlease try again")
            return redirect('customer-details', biller_name=biller_name, biller_code=biller_code)
    else:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            dict_result = res.json()
            categories = dict_result.get('data')
            return render(request, "home/customer-details.html", {"categories": categories})
        else:
            messages.add_message(
                request, messages.WARNING, "Bill Payment Error.\nPlease try again")
            return redirect('home-page')


def pay_bill(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        customer_id = request.POST.get("identifier")
        # customer_id = "08133913377"
        item_code = request.POST.get("item_code")
        biller_code = request.POST.get("biller_code")

        url = f"https://api.flutterwave.com/v3/billers/{biller_code}/items/{item_code}/payment"
        ref_id = str(uuid.uuid4())

    payload = {
        "country": "NG",
        "customer_id": customer_id,
        "amount": amount,
        "reference": ref_id,
        "callback_url": "https://webhook.site/5f9a659a-11a2-4925-89cf-8a59ea6a019a"
    }
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer FLWSECK_TEST-SANDBOXDEMOKEY-X",
        "Content-Type": "application/json"
    }

    res = requests.post(url, json=payload, headers=headers)
    print(res.status_code)
    if res.status_code == 200:
        dict_result = res.json()
        # confirm payment status
        # url = f"https://api.flutterwave.com/v3/bills/{ref_id}?verbose=1"
        url = f"https://api.flutterwave.com/v3/bills/{ref_id}"
        param = {"verbose": 1}
        response = requests.get(url, params=param, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            response_dict = response.json()
            data = response_dict.get('data')
            if data.get("code") == "200" and data.get("status") == "successful":
                flw_ref = data.get("flw_ref")
                tx_ref = data.get("tx_ref")
                batch_id = data.get("batch_id")
                transaction_date = data.get("transaction_date")
                customer_reference = data.get("customer_reference")
                amount = data.get("amount")
                customer_id = data.get("customer_id")
                product = data.get("product")

                # safe this info to a DB table
                # return redirect()


def product_details(request, product_name):
    prod = HomeAppliances.objects.get(name=product_name)
    if request.method == "POST":
        prod_qty = request.POST.get('quantity')
        if int(prod_qty) <= 0:
            messages.add_message(
                request, messages.WARNING, "Minimum quantity that can be added to cart is 1")
            previous_page = request.META.get('HTTP_REFERER')
            return redirect(previous_page)
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(
                user=request.user, paid=False)
        else:
            try:
                session = request.session['session_id']
            except:
                session = request.session['session_id'] = str(uuid.uuid4())
            cart, created = Cart.objects.get_or_create(
                session_id=session, paid=False)

        item = CartItems(cart=cart, home_appliance=prod,
                         quantity=prod_qty,)
        item_type, created = ProductType.objects.get_or_create(
            cart=cart, product_type="HomeAppliance")
        exist = False
        for prod in cart.cartitems.all():
            if prod.product:
                if item.home_appliance.name == prod.product.name:
                    existing_item = prod
                    existing_item.quantity = int(item.quantity)
                    existing_item.save()
                    exist = True
            elif prod.home_appliance:
                if item.home_appliance.name == prod.home_appliance.name:
                    existing_item = prod
                    existing_item.quantity = int(item.quantity)
                    existing_item.save()
                    exist = True
        if not exist:
            item.save()
            item_type.save()
        messages.add_message(request, messages.SUCCESS,
                             "Item has been added to Cart")
        return redirect("product-details", item.home_appliance.name)
    try:
        item = CartItems.objects.get(cart=cart, product=prod)
        item_qty = item.quantity
    except:
        item_qty = 1
    context = {"product": prod, "item_qty": item_qty}
    return render(request, "home/product-details.html", context)


def subscribe_newsletter(request):
    if request.method == "POST":
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            print('it is a valid form')
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Your subscription to our newletter was successful.")
        else:
            messages.add_message(
                request, messages.WARNING, "You have previously subscribed to our newletter.")
        return redirect('home-page')
    return HttpResponseForbidden()


def unsubscribe_newsletter(request):
    sub_email = NewsLetterSubscribers.objects.get(
        email=request.GET.get('email'))
    sub_email.delete()
    return render(request, 'user/unsubscribe-news.html')
