from django.contrib import admin
from .models import MyLocation


class MyLocationAdmin(admin.ModelAdmin):
    pass


admin.site.register(MyLocation, MyLocationAdmin)
