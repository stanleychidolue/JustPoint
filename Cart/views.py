from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from Estates.models import Estate, Shop
from Products.models import Product
from Cart.models import FavouriteEstateShops, FavouriteProducts
from django.db.utils import IntegrityError


from .views import FavouriteEstateShops, FavouriteProducts
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import json

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
