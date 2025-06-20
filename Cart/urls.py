from django.urls import path
from . import views


urlpatterns = [
    # cart functionalities urls
    path("view-cart", views.cart_page, name="cart-page"),
    path("add-to-cart/<option>/", views.add_to_cart, name="add-to-cart"),
    path("rm-from-cart/", views.rm_from_cart, name="rm-from-cart"),
    path("clear-cart/", views.delete_cart, name="delete-cart"),
    path("checkout/", views.checkout, name="checkout-page"),
    path("checkout/confirm-client-payment/",
         views.confirm_client_payment, name="confirm-client-payment"),
    path("checkout/payment-confirmation-failed/<order_id>/", views.payment_confirm_failed,
         name="payment-confirm-failed"),
    path("checkout/payment-confirmation-success/<order_id>/",
         views.payment_confirm_success, name="payment-confirm-success"),

    path("checkout/payment-confirmed/<order_id>/",
         views.payment_confirmed, name="payment-confirmed"),

    path("checkout/payment-confirmation-success/edit-delivery-address/<order_id>",
         views.edit_delivery_address, name="edit-delivery-address"),
    path("checkout/complete/", views.checkout_complete,
         name="checkout-complete-page"),
    path("payment-options/bank-transfer/",
         views.payment_options, name="payment-option"),

    # Favourite functionalities urls
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
