from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.conf import settings


class PlaceWidget(TextInput):

    def render(self, name, value, attrs=None, renderer=None):
        template = 'place_field/place_widget.html'

        text_input = super(PlaceWidget, self).render(
            name, value, attrs)
        if attrs:
            context = {
                'field_name': name,
                'field_input': mark_safe(text_input),
                'field_id': attrs['id']
            }
        else:
            context = {}
        return render_to_string(template, context)

    class Media:
        js = (
            "politicalplaces/js/politicalplaces.js",
            ("https://maps.googleapis.com/maps/api/js"
             "?language={}&key={}").format(
                settings.POLITICAL_MAP_LANGUAGE_CODE[:2], settings.GOOGLE_API_KEY),
        )
        css = {'all': ('politicalplaces/css/politicalplaces.css',)}
