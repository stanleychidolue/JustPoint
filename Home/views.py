from django.shortcuts import render, redirect
from .models import (Advertisement, UtilityPayment,
                     HomeAppliances, NewsLetters, NewsLetterSubscribers)
from .forms import NewsLetterForm
from django.core.cache import cache
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden


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


def subscribe_newsletter(request):
    if request.method == "POST":
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            print('it is a valid form')
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Your subscription to newletter was successful")
        else:
            messages.add_message(
                request, messages.ERROR, "Your subscription to newletter was not successful")
        return redirect('home-page')
    return HttpResponseForbidden()


def unsubscribe_newsletter(request):
    sub_email = NewsLetterSubscribers.objects.get(
        email=request.GET.get('email'))
    sub_email.delete()
    return render(request, 'user/unsubscribe-news.html')
