from django.urls import path
from . import views


urlpatterns = [
    path("view-all", views.estates, name="all-estate"),
    path("<estate>/shopsandvendors/", views.shops_vendors, name="shops&vendors"),

]
