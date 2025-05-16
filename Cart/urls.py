from django.urls import path
from . import views


urlpatterns = [
    # path("view-cart", views.cart_page, name="cart-page"),
    # path("add-to-cart/<option>/", views.add_to_cart, name="add-to-cart"),
    # path("rm-from-cart/", views.rm_from_cart, name="rm-from-cart"),
    # path("clear-cart/", views.delete_cart, name="delete-cart"),
    # path("checkout/", views.checkout, name="checkout-page"),
    # path("checkout/complete", views.checkout_complete,
    #      name="checkout-complete-page"),

    path("view-favourite/<option>/", views.favourite, name="favourite"),
    path("add-to-estate-favourite/",
         views.add_to_fav, name="add-to-fav"),

    path("rm-from-estate-favourite/",
         views.rm_from_fav, name="rm_from-fav"),
    path("add-to-product-favourite/",
         views.add_to_fav, name="add-to-fav"),

    path("rm-from-product-favourite/",
         views.rm_from_fav, name="rm_from-fav"),


]
