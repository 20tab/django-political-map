from django.contrib import admin
from .models import MyLocation


class MyLocationAdmin(admin.ModelAdmin):

    def country(obj):
        return obj.place.country

    list_display = ('place', country)


admin.site.register(MyLocation, MyLocationAdmin)
