from django.contrib import admin
from .models import MapItem, PoliticalPlace


class PoliticalPlaceAdmin(admin.ModelAdmin):

    def refresh_data(modeladmin, request, queryset):
        for place in queryset:
            place.refresh_data()

    actions = [refresh_data]
    list_display = [
        'address', 'geo_type', 'continent', 'country', 'geocode', 'place_id']
    list_filter = ['continent', 'geo_type']
    search_fields = [
        'place_id', 'address', 'continent', 'country',
        'administrative_area_level_1',
        'administrative_area_level_2']
    ordering = ('continent', 'country', 'address')


class MapItemAdmin(admin.ModelAdmin):
    list_display = [
        'long_name', 'short_name', 'place_id',
        'geo_type', 'geocode', 'slug', 'url']
    list_filter = ['geo_type']
    search_fields = [
        'place_id', 'long_name', 'short_name',
        'geo_type', 'geocode', 'slug', 'url']
    ordering = ('geo_type', 'long_name')


admin.site.register(PoliticalPlace, PoliticalPlaceAdmin)
admin.site.register(MapItem, MapItemAdmin)
