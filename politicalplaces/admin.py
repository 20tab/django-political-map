from django.contrib import admin
from .models import MapItem, PoliticalPlace
#from .forms import PoliticalPlaceForm


class PoliticalPlaceAdmin(admin.ModelAdmin):
    pass
    #form = PoliticalPlaceForm


admin.site.register(PoliticalPlace, PoliticalPlaceAdmin)
admin.site.register(MapItem)
