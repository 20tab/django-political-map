from django.contrib import admin
from .models import MyLocation, MyLocationMultiPlace


class MyLocationAdmin(admin.ModelAdmin):

    def country(obj):
        return obj.place.country

    list_display = ('place', country)


class MyLocationMultiPlaceAdmin(admin.ModelAdmin):

    list_display = ('place1', 'place2')


admin.site.register(MyLocation, MyLocationAdmin)
admin.site.register(MyLocationMultiPlace, MyLocationMultiPlaceAdmin)
