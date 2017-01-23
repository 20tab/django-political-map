from __future__ import unicode_literals

from django.test import TestCase, override_settings
from .models import PoliticalPlace, MapItem
from .utils import country_to_continent
from .backends import Client
from .exceptions import GeoTypeException, NoResultsException
from .widgets import PlaceWidget
from googlemaps.exceptions import HTTPError


class PlaceWidgetTest(TestCase):

    def setUp(self):
        self.placewidget = PlaceWidget()

    def test_place_widget_media(self):
        self.assertEqual(
            str(self.placewidget.media),
            ('<script type="text/javascript" '
             'src="/static/politicalplace/js/politicalplace.js">'
             '</script>'),)

    def test_place_widget_render(self):
        self.assertEqual(
            str(self.placewidget.render('myfield', 'myvalue')),
            ('<input name="myfield" type="text" value="myvalue" />\n'
             '<div class="place-widget" style="margin-top: 4px">\n    '
             '<label></label>\n    <div id="map_myfield" '
             'style="width: 500px; height: 250px"></div>\n</div>\n')
        )


class BackendTest(TestCase):

    def test_init_client(self):
        from .backends import googlemaps
        self.assertTrue(googlemaps.Client)

    @override_settings(LANGUAGE_CODE='en-us')
    def test_geocode(self):
        client = Client()
        res = client.geocode("Roma, IT")
        self.assertEqual(
            "Rome, Italy",
            res[0]['formatted_address'])


class UtilsTest(TestCase):

    def test_country_to_continent(self):
        self.assertEqual(
            "Europe", country_to_continent("Italy"))
        self.assertEqual(
            "Africa", country_to_continent("Senegal"))
        self.assertEqual(
            "South America", country_to_continent("Colombia"))

    def test_country_to_continent_none(self):
        self.assertFalse(country_to_continent("Klingon"))


class PoliticalPlaceModelTest(TestCase):

    def setUp(self):
        self.test_place = PoliticalPlace(
            address="via Luigi Gastinelli 118, Rome, Italy")
        self.test_place_wrong_addr = PoliticalPlace(
            address="qwertyuiop")

    def test_unicode_str(self):
        test_place = PoliticalPlace.get_or_create_from_address(
            self.test_place.address)
        self.assertEqual(
            str(test_place),
            "Via Luigi Gastinelli, 118, 00132 Roma RM, Italy")

    def test_latlng_property_empty_geocode(self):
        self.assertFalse(self.test_place.lat)
        self.assertFalse(self.test_place.lng)

    def test_political_place_create_map_items(self):
        self.test_place.continent = 'Europe'
        self.test_place.country = 'Italy'
        self.test_place.administrative_area_level_1 = 'Lazio'
        client = Client()
        lat = '41.6552418'
        lng = '12.989615'
        self.test_place._create_map_items(client, lat, lng)
        self.assertEqual(
            "Europe", self.test_place.continent_item.long_name)
        self.assertEqual(
            "Italy", self.test_place.country_item.long_name)
        self.assertEqual(
            "Lazio",
            self.test_place.administrative_area_level_1_item.long_name)
        self.assertFalse(
            self.test_place.administrative_area_level_2_item)
        self.assertFalse(
            self.test_place.administrative_area_level_3_item)
        self.assertFalse(
            self.test_place.locality_item)
        self.assertFalse(
            self.test_place.sublocality_item)

    def test_political_place_create_map_items_no_continent(self):
        self.test_place.country = 'Italy'
        client = Client()
        lat = '41.6552418'
        lng = '12.989615'
        self.test_place._create_map_items(client, lat, lng)
        self.assertEqual(
            "Italy", self.test_place.country_item.long_name)

    def test_political_place_get_or_create_from_address_fields_creation(self):
        test_place = PoliticalPlace.get_or_create_from_address(
            self.test_place.address)
        self.assertEqual(
            test_place.administrative_area_level_1,
            "Lazio")
        self.assertEqual(
            test_place.country,
            "Italy")

    def test_political_place_get_or_create_from_address_items_creation(self):
        test_place = PoliticalPlace.get_or_create_from_address(
            self.test_place.address)
        self.assertEqual(
            test_place.administrative_area_level_1_item.long_name,
            "Lazio")
        self.assertEqual(
            test_place.country_item.short_name,
            "IT")

    def test_political_place_process_address_wrong(self):
        with self.assertRaises(NoResultsException):
            PoliticalPlace.get_or_create_from_address(
                self.test_place_wrong_addr.address)

    def test_political_place_link_map_items(self):
        self.test_place.geocode = "41.6552418,12.989615"
        self.test_place.place_id = ""
        self.test_place.address = "Lazio, Italy"
        self.test_place.country = "Italy"
        self.test_place.administrative_area_level_1 = "Lazio"
        self.test_place.link_map_items()
        self.assertEqual(
            self.test_place.administrative_area_level_1_item.long_name,
            "Lazio")
        self.assertEqual(
            self.test_place.country_item.short_name,
            "IT")
        self.assertEqual(
            self.test_place.continent_item.long_name,
            "Europe")


class MapItemModelTest(TestCase):

    def setUp(self):
        self.test_item = MapItem.get_or_create_from_address(
            "Lazio, Italy", 'administrative_area_level_1')

    def test_unicode_str(self):
        self.assertEqual(
            str(self.test_item),
            "Lazio(administrative_area_level_1)")

    def test_get_or_create_from_place_id_create(self):
        place_id = "ChIJNWU6NebuJBMRKYWj8WSQSm8"
        map_item = MapItem.get_or_create_from_place_id(place_id)
        self.assertEqual(map_item.long_name, "Lazio")
        self.assertEqual(map_item.short_name, "Lazio")
        self.assertEqual(map_item.geo_type, "administrative_area_level_1")
        self.assertEqual(
            map_item.types, "administrative_area_level_1,political")
        self.assertEqual(map_item.geocode, "41.6552418,12.989615")
        self.assertEqual(
            map_item.place_id,
            'ChIJNWU6NebuJBMRKYWj8WSQSm8')

    def test_get_or_create_from_place_id_error(self):
        place_id = "qwertyuiop"
        with self.assertRaises(HTTPError):
            MapItem.get_or_create_from_place_id(place_id)

    def test_get_or_create_from_address_create(self):
        address = "Lazio, Italy"
        map_item = MapItem.get_or_create_from_address(
            address, 'administrative_area_level_1')
        self.assertEqual(map_item.long_name, "Lazio")
        self.assertEqual(map_item.short_name, "Lazio")
        self.assertEqual(map_item.geo_type, "administrative_area_level_1")
        self.assertEqual(
            map_item.types, "administrative_area_level_1,political")
        self.assertEqual(map_item.geocode, "41.6552418,12.989615")
        self.assertEqual(
            map_item.place_id,
            'ChIJNWU6NebuJBMRKYWj8WSQSm8')

    def test_get_or_create_from_address_error(self):
        address = "qwertyuiop"
        with self.assertRaises(NoResultsException):
            MapItem.get_or_create_from_address(
                address, 'administrative_area_level_1')

    def test_get_or_create_from_address_wrong_geo_type(self):
        address = "Lazio, Italy"
        with self.assertRaises(GeoTypeException):
            MapItem.get_or_create_from_address(
                address, 'country')

    def test_get_or_create_from_address_get(self):
        self.assertEqual(1, MapItem.objects.count())
        address = "Calabria, Italy"
        MapItem.get_or_create_from_address(
            address, 'administrative_area_level_1')
        self.assertEqual(2, MapItem.objects.count())
        MapItem.get_or_create_from_address(
            address, 'administrative_area_level_1')
        self.assertEqual(2, MapItem.objects.count())

    def test_get_or_create_from_address_africa(self):
        address = "Kayuma"
        map_item = MapItem.get_or_create_from_address(
            address, 'locality')
        self.assertEqual(map_item.long_name, "Kayuma")
        self.assertEqual(map_item.short_name, "Kayuma")
        self.assertEqual(map_item.geocode, "-9.383333,21.833333")
        self.assertEqual(
            map_item.place_id,
            'ChIJ4_CniEcdKxoRb3-I6gCh7II')

    def test_get_or_create_from_address_america(self):
        address = "Dosquebradas, Pereira"
        map_item = MapItem.get_or_create_from_address(
            address, 'locality')
        self.assertEqual(map_item.long_name, "Dosquebradas")
        self.assertEqual(map_item.short_name, "Dosquebradas")
        self.assertEqual(map_item.geocode, "4.8318256,-75.68056779999999")
        self.assertEqual(
            map_item.place_id,
            'ChIJhyRrTd-AOI4ReAs5SWb4f5s')

    def test_get_or_create_from_address_asia(self):
        address = "Tokachi District, Japan"
        map_item = MapItem.get_or_create_from_address(
            address, 'locality')
        self.assertEqual(map_item.long_name, "Tokachi District")
        self.assertEqual(map_item.short_name, "Tokachi District")
        self.assertEqual(map_item.geocode, "42.913886,143.6932779")
        self.assertEqual(
            map_item.place_id,
            'ChIJF1BfXpK2c18R4BivzcAmO9M')

    def test_get_or_create_from_address_europe(self):
        address = "Hordaland, Norway"
        map_item = MapItem.get_or_create_from_address(
            address, 'administrative_area_level_1')
        self.assertEqual(map_item.long_name, "Hordaland")
        self.assertEqual(map_item.short_name, "Hordaland")
        self.assertEqual(map_item.geocode, "60.2733674,5.7220194")
        self.assertEqual(
            map_item.place_id,
            'ChIJU9YJbagwPEYR0ByzKCZ3AQM')

    def test_get_or_create_from_address_oceania(self):
        address = "Tonga"
        map_item = MapItem.get_or_create_from_address(
            address, 'country')
        self.assertEqual(map_item.long_name, "Tonga")
        self.assertEqual(map_item.short_name, "TO")
        self.assertEqual(map_item.geocode, "-21.178986,-175.198242")
        self.assertEqual(
            map_item.place_id,
            'ChIJHdCfu0S2k3ERqeJexcrMbfM')
