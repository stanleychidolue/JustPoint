from django.contrib import admin
from .models import Advertisement

# Register your models here.


class AdvertAdmin(admin.ModelAdmin):
    list_display=("advert_title","advert_location")










admin.site.register(Advertisement,AdvertAdmin)