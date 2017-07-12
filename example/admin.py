from django.contrib import admin
from .models import (
    MyLocation, MyLocationMultiPlace,
    MyLocationInlineTest, MyLocationInlinePlace,
    MyLocationInlineNotPlace, MyLocationComplex)


class MyLocationInlinePlaceAdmin(admin.TabularInline):
    model = MyLocationInlinePlace


class MyLocationInlineNotPlaceAdmin(admin.TabularInline):
    model = MyLocationInlineNotPlace


class MyLocationAdmin(admin.ModelAdmin):

    def country(obj):
        if obj.place:
            return obj.place.country
        return None

    list_display = ('place', country)


class MyLocationMultiPlaceAdmin(admin.ModelAdmin):

    list_display = ('place1', 'place2')


class MyLocationInlineAdmin(MyLocationAdmin):

    inlines = [MyLocationInlinePlaceAdmin, MyLocationInlineNotPlaceAdmin]


admin.site.register(MyLocation, MyLocationAdmin)
admin.site.register(MyLocationMultiPlace, MyLocationMultiPlaceAdmin)
admin.site.register(MyLocationInlineTest, MyLocationInlineAdmin)
admin.site.register(MyLocationComplex, MyLocationAdmin)
