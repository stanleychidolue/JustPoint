from django.contrib import admin
from .models import (Advertisement, UtilityPayment,
                     HomeAppliances, NewsLetterSubscribers, NewsLetters)

# Register your models here.


class AdvertAdmin(admin.ModelAdmin):
    list_display = ("advert_title",)


admin.site.register(Advertisement, AdvertAdmin)
admin.site.register(UtilityPayment)
admin.site.register(HomeAppliances)
admin.site.register(NewsLetterSubscribers)
admin.site.register(NewsLetters)
