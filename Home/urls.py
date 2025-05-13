from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home-page"),
    path('<service>/', views.services, name="service-page"),
    path("utility-payment/paybill/", views.pay_bill, name="pay-bill"),
    path("utility-payment/<utility_category>/",
         views.utility_payment, name='utility-payment'),
    path("utility-payment/<biller_name>/<biller_code>/",
         views.validate_customer_details, name='customer-details'),
    path("product-details/<product_name>/",
         views.product_details, name="product-details"),
    path('subscribe-newsletter/', views.subscribe_newsletter,
         name='subscribe-newsletter'),
    path('unsubscribe-newsletter/', views.unsubscribe_newsletter,
         name='unsubscribe-newsletter'),
]
