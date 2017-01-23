from django.test import TestCase
from django.forms import ModelForm
from politicalplaces.models import PoliticalPlace, MapItem
from .models import MyLocation


class MyLocationTest(TestCase):

    def setUp(self):
        class MyLocationForm(ModelForm):

            class Meta:
                model = MyLocation
                exclude = []
        self.modelform = MyLocationForm()

    def test_mylocation_creation(self):
        self.assertEqual(0, PoliticalPlace.objects.count())
        self.assertEqual(0, MapItem.objects.count())
        self.assertEqual(0, MyLocation.objects.count())
        loc = MyLocation()
        loc.name = "Test Location"
        place = PoliticalPlace.get_or_create_from_address(
            address='via Luigi Gastinelli, Rome')
        loc.place = place
        loc.save()
        self.assertEqual(
            loc.place.country_item.short_name,
            "IT")
        self.assertEqual(1, PoliticalPlace.objects.count())
        self.assertEqual(5, MapItem.objects.count())
        self.assertEqual(1, MyLocation.objects.count())
        loc2 = MyLocation()
        loc2.name = "Test Location 2"
        place2 = PoliticalPlace.get_or_create_from_address(
            address='via Luigi Gastinelli, Rome')
        loc2.place = place2
        loc2.save()
        self.assertEqual(
            loc2.place.country_item.short_name,
            "IT")
        self.assertEqual(1, PoliticalPlace.objects.count())
        self.assertEqual(5, MapItem.objects.count())
        self.assertEqual(2, MyLocation.objects.count())

    def test_mylocation_form(self):
        self.assertHTMLEqual(
            """<tr><th><label for="id_place">Place:</label></th><td><input id="id_place" name="place" type="text" />
<div class="place-widget" style="margin-top: 4px">
    <label></label>
    <div id="map_place" style="width: 500px; height: 250px"></div>
</div>
</td></tr>""",
            str(self.modelform)
        )

    def test_mylocation_form_media(self):
        self.assertHTMLEqual(
            ('<script type="text/javascript" src='
             '"/static/politicalplace/js/politicalplace.js"></script>'),
            str(self.modelform.media)
        )
