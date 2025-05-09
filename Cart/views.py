from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from Estates.models import Estate, Shop
from Cart.models import FavouriteEstateShops
from django.db.utils import IntegrityError
from .views import FavouriteEstateShops
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import json

# Create your views here.


# @login_required
def favourite(request, option):
    fav_shops = []
    if request.user.is_authenticated:
        if option == "estate":
            estate_fav = FavouriteEstateShops.objects.filter(user=request.user)
            fav_shops = [saved.shop for saved in estate_fav]
    else:
        messages.add_message(
            request, messages.WARNING, "You need to be logged in to view your favourites")
        return redirect("/user/login/?next=/customer/view-favourite/estate/")

    return render(request, "cart&fav/favourite.html", {f"{option}": True, 'fav_shops': fav_shops})


def add_to_estate_fav(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status_code": 401, "message": "user_not_authenticated"})
    data = json.loads(request.body)
    data_id = data['id']

    shop = Shop.objects.get(id=data_id)

    item = FavouriteEstateShops(user=request.user, shop=shop)

    try:
        item.save()
    except IntegrityError:
        return JsonResponse({"status_code": 400, "message": "item_already_saved"})

    response = {"status_code": 200, "message": "Saved Successfully"}
    return JsonResponse(response)


def rm_from_estate_fav(request):
    data = json.loads(request.body)
    id = data['id']
    # shop = Shop.objects.get(id=id)

    item = FavouriteEstateShops.objects.get(user=request.user, shop=id)
    # shop = Shop.objects.get(user=request.user,product_id=id)
    # usr_saved_items=SavedItems.objects.filter(user=request.user)
    item.delete()
    response = {"message": "Removed Successfully"}
    return JsonResponse(response)
