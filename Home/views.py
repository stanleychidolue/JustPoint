from django.shortcuts import render
from .models import Advertisement
from django.core.cache import cache


# Create your views here.

CACHE_TIMEOUT = 60*10


def home(request):

    all_adds = cache.get_or_set(
        "all_adds", Advertisement.objects.all(), CACHE_TIMEOUT).order_by('id')
    context = {
        "carousel": all_adds.filter(advert_location="CAROUSEL"),
    }
    return render(request, "home/index.html", context)
