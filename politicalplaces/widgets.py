from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class PlaceWidget(TextInput):

    def render(self, name, value, attrs=None):
        template = 'place_field/place_widget.html'
        text_input = super(PlaceWidget, self).render(
            name, value, attrs)
        return render_to_string(template, {
            'field_name': name,
            'field_input': mark_safe(text_input)
        })

    class Media:
        js = (
            "https://maps.googleapis.com/maps/api/js?libraries=places",
            "https://ajax.googleapis.com/ajax/libs/jquery/1.6/jquery.min.js",
            "politicalplaces/js/store-locator.min.js",
            "politicalplaces/js/politicalplaces.js",)
        css = {'all': ('politicalplaces/css/storelocator.css',)}
