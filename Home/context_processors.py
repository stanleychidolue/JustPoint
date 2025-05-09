from Estates.models import Estate
from .forms import NewsLetterForm
from django.core.cache import cache
from django.core.paginator import Paginator

CACHE_TIMEOUT = 60*10

form = NewsLetterForm()


def base_request(request):
    estates = cache.get_or_set(
        "estates", Estate.objects.all(), CACHE_TIMEOUT).order_by('id')
    estate_paginator = Paginator(estates, 10)  # Show 10 products per page.
    page_number = request.GET.get("page")
    estate_page_obj = estate_paginator.get_page(page_number)
    context = {
        "newsletterform": form,
        "estates": estate_page_obj,
    }
    return context
