from Estates.models import Estate
from .forms import NewsLetterForm
from django.core.cache import cache
from django.core.paginator import Paginator
from Cart.models import Cart
import uuid

CACHE_TIMEOUT = 60*10

form = NewsLetterForm()


def base_request(request):
    user = request.user
    if user.is_authenticated:
        try:
            cart = Cart.objects.get(user=user, paid=False)
        except:
            cart = {"num_of_item": 0}
    else:
        try:
            session = request.session['session_id']
        except:
            request.session['session_id'] = str(uuid.uuid4())
            session = request.session.get('session_id')
        finally:
            try:
                cart = Cart.objects.get(session_id=session, paid=False)
            except:
                cart = {"num_of_item": 0}

    estates = cache.get_or_set(
        "estates", Estate.objects.all(), CACHE_TIMEOUT).order_by('id')
    estate_paginator = Paginator(estates, 10)  # Show 10 products per page.
    page_number = request.GET.get("page")
    estate_page_obj = estate_paginator.get_page(page_number)

    #  To get the different cart items and there retaltionships
    cart_items = {"products": [], "home_appliances": [], "market_product": []}
    if type(cart) != dict:
        for item in cart.cartitems.all():
            if item.product:
                cart_items["products"].append(item)
            elif item.home_appliance:
                cart_items["home_appliances"].append(item)

    context = {
        "newsletterform": form,
        "estates": estate_page_obj,
        "cart": cart,
        "cart_items": cart_items,
    }

    return context
