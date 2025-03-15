from django.urls import path
from . import views

urlpatterns = [
path(" ", views.new_function,name="route_name(blog-home)")
]
