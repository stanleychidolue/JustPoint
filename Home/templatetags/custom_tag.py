from django.template.defaulttags import register
from django.template.defaultfilters import stringfilter
from itertools import islice
import babel.numbers


@register.filter
def check_prime(number):
    return not number % 2 == 0


@register.filter
def get_currency(amount):
    return babel.numbers.format_currency(amount, "NGN", locale='en_NG')[:-3]
    # pass


@register.filter
def currency(amount):
    try:
        output = get_currency(amount)
    except:
        output = amount
    return output


# from django import template
# register = template.Library()

@register.filter
def index(list, i):
    return list[i]


@register.filter
def split_dict(dictionary, i):
    inc = iter(dictionary.items())
    res1 = dict(islice(inc, len(dictionary) // 2)).items()
    res2 = dict(inc).items()
    if i == 0:
        return res1
    else:
        return res2


@register.filter
def check_product_type(item, type):
    if item.product and type == "Estate":
        return True
    elif item.home_appliance and type == "Market":
        return True
    else:
        return False


@register.filter
def get_product_property(item, property):
    if item.product:
        return eval(f"item.product.{property}")
    elif item.home_appliance:
        return eval(f"item.home_appliance.{property}")
