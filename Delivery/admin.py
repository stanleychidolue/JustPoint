from django.contrib import admin
from .models import DispatchRider

# Register your models here.


class DispatchRiderAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email",
                    "dispatch_type", "rider_location"]
    list_filter = ('rider_location', "dispatch_type")
    search_fields = ("user__email__icontains",)
    list_per_page = 10


admin.site.register(DispatchRider, DispatchRiderAdmin)
