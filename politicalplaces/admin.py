from django.contrib import admin
from .models import MapItem, PoliticalPlace


class PoliticalPlaceAdmin(admin.ModelAdmin):

    def refresh_data(modeladmin, request, queryset):
        for place in queryset:
            place.refresh_data()

    actions = (refresh_data,)
    list_display = (
        'address', 'geo_type', 'continent', 'country', 'geocode', 'place_id')
    list_filter = ('continent', 'geo_type')
    search_fields = (
        'place_id', 'address', 'continent', 'country',
        'administrative_area_level_1', 'administrative_area_level_2',
        'administrative_area_level_3', 'administrative_area_level_4',
        'administrative_area_level_5', 'locality', 'ward',
        'sublocality', 'neighborhood')
    ordering = ('continent', 'country', 'address')
    raw_id_fields = (
        'continent_item', 'country_item', 'administrative_area_level_1_item',
        'administrative_area_level_2_item', 'administrative_area_level_3_item',
        'administrative_area_level_4_item', 'administrative_area_level_5_item',
        'locality_item', 'ward_item', 'sublocality_item', 'neighborhood_item',
        'self_item')


class MapItemAdmin(admin.ModelAdmin):
    list_display = (
        'long_name', 'short_name', 'place_id', 'geo_type', 'geocode',
        'slug', 'relative_url', 'parent', 'error_log')
    list_filter = ('geo_type',)
    search_fields = (
        'place_id', 'long_name', 'short_name',
        'geo_type', 'geocode', 'slug', 'url', 'error_log')
    ordering = ('geo_type', 'long_name')
    raw_id_fields = ('parent',)


admin.site.register(PoliticalPlace, PoliticalPlaceAdmin)
admin.site.register(MapItem, MapItemAdmin)
