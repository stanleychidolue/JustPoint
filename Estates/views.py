from django.shortcuts import render
from .models import Shop, Estate
from Cart.models import FavouriteEstateShops

# Create your views here.


def estates(request):
    return render(request, 'estate/estates.html')


def shops_vendors(request, estate):
    estate = Estate.objects.get(name=estate)
    estate_id = estate.pk
    estate_shops = Shop.objects.filter(estate=estate_id)
    if request.user.is_authenticated:
        estate_fav = FavouriteEstateShops.objects.filter(user=request.user)
        fav_shops = [saved.shop for saved in estate_fav]
    else:
        fav_shops = []

    return render(request, "estate/shops&vendors.html", {'estate_shops': estate_shops, "fav_shops": fav_shops})
