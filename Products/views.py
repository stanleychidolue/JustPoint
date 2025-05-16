from unicodedata import category
from django.shortcuts import render
from Products.models import Product
from Estates.models import Estate, Shop
from Cart.models import FavouriteProducts

from django.http import HttpResponse, JsonResponse
import json


# Create your views here.


def products_page(request, shop_type, shop_name):
    shop = Shop.objects.get(name=shop_name)
    all_products = Product.objects.filter(
        shop=shop.pk).order_by("product_category")

    category_dict = {}
    for prod in all_products:
        if category_dict.get(prod.product_category) != None:
            category_dict[prod.product_category].append(prod)
        else:
            category_dict[prod.product_category] = []
            category_dict[prod.product_category].append(prod)

    if request.user.is_authenticated:
        product_fav = FavouriteProducts.objects.filter(user=request.user)
        fav_products = [saved.product for saved in product_fav]
    else:
        fav_products = []

    print(fav_products)
    context = {"products": all_products,
               "shop_name": shop.name, "shop_type": shop_type, "category_dict": category_dict,
               "fav_products": fav_products}

    return render(request, "product/products.html", context)


def search(request):
    data = json.loads(request.body)
    search_in = data.get("searchLocation")
    typed_letters = data.get("lettersTyped")
    name = data.get("id")
    res_dict = {}
    if search_in == "products":
        shop = Shop.objects.get(name=name)
        contains = Product.objects.filter(
            shop=shop.pk, name__icontains=typed_letters).order_by("product_category")
        # starts_with = all_products.filter(name__startswith=typed_letters)
        res_dict = {"contains": []}
        for item in contains:
            res_dict["contains"].append(f"{item.name} ₦{item.price}")
    elif search_in == "shops":
        contains = Shop.objects.filter(name__icontains=typed_letters)
        res_dict = {"contains": []}
        for item in contains:
            res_dict["contains"].append(f"{item.name}")
    elif search_in == "services":
        contains = Estate.objects.filter(name__icontains=typed_letters)
        res_dict = {"contains": []}
        for item in contains:
            res_dict["contains"].append(f"{item.name}")

    return JsonResponse(res_dict)


def search_page(request, shop_name=None):
    search_query = request.GET.get("search-query")
    search_in = request.GET.get("search-location")
    if search_in == "products":
        shop = Shop.objects.get(name=shop_name)
        contains = Product.objects.filter(
            shop=shop.pk, name__icontains=search_query).order_by("product_category")
        context = {"search_result": contains,
                   "search_query": search_query, "type": search_in}
    elif search_in == "services":
        estate_contains = Estate.objects.filter(name__icontains=search_query)
        context = {"search_result": [estate_contains],
                   "search_query": search_query, "type": search_in}
    return render(request, "product/search-page.html", context)
