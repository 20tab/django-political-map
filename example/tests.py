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
        self.MyLocationForm = MyLocationForm

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

    def test_mylocation_formfield_clean(self):
        self.assertEqual(0, PoliticalPlace.objects.count())
        post_data = {'place': 'via Luigi Gastinelli 118, Rome'}
        location_form = self.MyLocationForm(data=post_data)
        location_form.save()
        self.assertEqual(1, PoliticalPlace.objects.count())

    def test_mylocation_formfield_prepare_value(self):
        test_place = PoliticalPlace.get_or_create_from_address(
            address='via Luigi Gastinelli, Rome')
        location = MyLocation(place=test_place)
        location.save()
        location_form = self.MyLocationForm(instance=location)
        self.assertEqual(
            location_form['place'].value(),
            "Via Luigi Gastinelli, 00132 Roma, Italy")

    def test_mylocation_formfield_prepare_value_no_instance(self):
        location_form = self.MyLocationForm()
        self.assertEqual(
            location_form['place'].value(), None)

    def test_mylocation_null(self):
        my_location = MyLocation.objects.create()
        self.assertTrue(my_location)
