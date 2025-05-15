from django.urls import path
from . import views


urlpatterns = [
    # path("view-all", views.estates, name="all-estate"),
    path("<shop_type>/<shop_name>/", views.products_page, name="products-page"),
    path("search/", views.search, name='search'),
    path("search/<shop_name>", views.search_page, name='search-page'),
    

]
