"""
URL configuration for JustPoint project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = "JustPoint Administration"
admin.site.site_title = "JustPoint Administration"
admin.site.index_title = "JustPoint Admin"
admin.site.empty_value_display = "(None)"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Home.urls")),
    path("user/", include("User.urls")),
    path("estates/", include("Estates.urls")),
    path('customer/', include('Cart.urls')),
    path('products/', include('Products.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
