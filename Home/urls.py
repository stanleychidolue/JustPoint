from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home-page"),
    path('subscribe-newsletter/', views.subscribe_newsletter,
         name='subscribe-newsletter'),
    path('unsubscribe-newsletter/', views.unsubscribe_newsletter,
         name='unsubscribe-newsletter'),
]
