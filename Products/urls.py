from django.urls import path
from . import views


urlpatterns = [
    path("search/", views.search, name='search'),
    path("search/<shop_name>/", views.search_page, name='search-page'),
    path("search/", views.search_page, name='search-page2'),
    path("<shop_type>/<shop_name>/", views.products_page, name="products-page"),

]
