from django.shortcuts import render, redirect
from .models import (Advertisement, UtilityPayment,
                     HomeAppliances, NewsLetters, NewsLetterSubscribers)
from .forms import NewsLetterForm
from django.core.cache import cache
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
import requests
import os


# Create your views here.

CACHE_TIMEOUT = 60*10


def home(request):

    all_ads = cache.get_or_set(
        "all_ads", Advertisement.objects.all(), CACHE_TIMEOUT).order_by('id')
    all_utility = cache.get_or_set(
        "all_utililty", UtilityPayment.objects.all(), CACHE_TIMEOUT).order_by('id')
    all_appliance = cache.get_or_set(
        "all_appliance", HomeAppliances.objects.all(), CACHE_TIMEOUT).order_by('id')
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

    # url = f"https://api.flutterwave.com/v3/bills/{utility_category}/billers?country=NG"

    # headers = {
    #     "accept": "application/json",
    #     "Authorization": "Bearer FLWSECK_TEST-SANDBOXDEMOKEY-X",
    #     "Content-Type": "application/json"
    # }

    url = f"https://qa.interswitchng.com/quicktellerservice/api/v5/services"

    headers = {
        "Authorization": f"Bearer {os.environ.get('ACCESS_TOKEN')}",
        "TerminalId": os.environ.get("TEST_TERMINAL_ID"),
        "Content-Type": "application/json"
    }
    try:
        res = requests.get(url, headers=headers)
    except:
        print('an error occured')
    print(res.text)
    print(res.status_code)
    print(res.json())
    if res.status_code == 200:
        dict_result = res.json()
        categories = dict_result.get('data')
        print(categories)
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
        sub_plan = request.POST.get('subscription-plan')
        sub_plan = sub_plan.split(",")
        biller_code = request.POST.get('biller_code')
        print(identifier)
        url = f"https://api.flutterwave.com/v3/bill-items/{sub_plan[0]}/validate?"

        param = {"customer": identifier, }
        res = requests.get(url, headers=headers, params=param)
        if res.status_code == 200:
            print(res.status_code)
            dict_result = res.json()
            info = dict_result.get('data')
            print(info)
            context = {"customer_info": info,
                       "sub_plan": sub_plan, "biller_code": biller_code}
            return render(request, 'home/confirm-details.html', context)
        else:
            print(f"incorrect iuc number", res.status_code)
    else:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            dict_result = res.json()
            categories = dict_result.get('data')
            print(categories)
            return render(request, "home/customer-details.html", {"categories": categories})
        else:
            messages.add_message(
                request, messages.WARNING, "Bill Payment Error.\nPlease try again")
            # return redirect('utility-payment')


def product_details(request, product_name):
    prod = HomeAppliances.objects.get(appliance_name=product_name)
    return render(request, "home/product-details.html", {"product": prod})


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
