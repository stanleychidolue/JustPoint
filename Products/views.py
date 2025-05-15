from unicodedata import category
from django.shortcuts import render
from Products.models import Product
from Estates.models import Shop

import json
from django.http import HttpResponse, JsonResponse


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

    context = {"products": all_products,
               "shop_name": shop.name, "shop_type": shop_type, "category_dict": category_dict}

    return render(request, "product/products.html", context)


def search(request):
    data = json.loads(request.body)
    search_in = data.get("searchLocation")
    typed_letters = data.get("lettersTyped")
    name = data.get("id")
    res_dict = {}
    if search_in == "products":
        shop = Shop.objects.get(name=name)
        all_products = Product.objects.filter(
            shop=shop.pk).order_by("product_category")
        # starts_with = all_products.filter(name__startswith=typed_letters)
        contains = all_products.filter(name__icontains=typed_letters)
        # starts_with = contains.filter(name__startswith=typed_letters)
        res_dict = {"contains": []}
        for item in contains:
            res_dict["contains"].append(f"{item.name} ₦{item.price}")
    elif search_in == "shops":
        all_shops = Shop.objects.all()
        contains = all_shops.filter(name__icontains=typed_letters)
        res_dict = {"contains": []}
        for item in contains:
            res_dict["contains"].append(f"{item.name}")

    return JsonResponse(res_dict)


def search_page(request, shop_name=None):

    search_query = request.GET.get("search-query")
    search_in = request.GET.get("search-location")
    if search_in == "products":
        shop = Shop.objects.get(name=shop_name)
        all_products = Product.objects.filter(
            shop=shop.pk).order_by("product_category")

        contains = all_products.filter(name__icontains=search_query)

    return render(request, "product/search-page.html", {"search_result": contains, "search_query": search_query, "type": search_in})
