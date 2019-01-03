from __future__ import unicode_literals

from django.test import TestCase, override_settings
from unittest import skip
from .models import PoliticalPlace, MapItem
from .utils import country_to_continent
from .backends import Client
from .exceptions import NoResultsException  # GeoTypeException
from .widgets import PlaceWidget
# from .forms import PoliticalPlaceForm
from googlemaps.exceptions import HTTPError

import json


class PlaceWidgetTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.placewidget = PlaceWidget()

    def test_place_widget_media(self):
        self.assertHTMLEqual(
            str(self.placewidget.media),
            """<link href="/static/politicalplaces/css/politicalplaces.css" type="text/css" media="all" rel="stylesheet" />
<script type="text/javascript" src="/static/politicalplaces/js/politicalplaces.js"></script>
<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?language=en&amp;key=AIzaSyBUSalEfGXgegMLzcZGSx45YT01okoRfOs"></script>"""  # noqa
        )

    def test_place_widget_render(self):
        self.assertHTMLEqual(
            str(self.placewidget.render(
                'myfield', 'myvalue', attrs={'id': 'idtest'})),
            """<div class="politicalplace-widget widget" data-id="idtest" data-name="myfield">
            <input id='idtest' name="myfield" type="text" value="myvalue" />
            <a class='widget__search button' id="search_map_idtest">Search</a>
<div class="widget__place">
    <div class='widget__place__panel' id="panel_idtest"></div>
    <div class='widget__place__map' id="map_canvas_idtest"></div>
</div>
"""
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
            "Rome, Metropolitan City of Rome, Italy",
            res[0]['formatted_address'])


class UtilsTest(TestCase):

    def test_country_to_continent(self):
        self.assertEqual(
            "Europe", country_to_continent("Italy"))
        self.assertEqual(
            "Europe", country_to_continent("Czechia"))
        self.assertEqual(
            "Africa", country_to_continent("Senegal"))
        self.assertEqual(
            "South America", country_to_continent("Colombia"))

    def test_country_to_continent_none(self):
        self.assertFalse(country_to_continent("Klingon"))


class PoliticalPlaceModelTest(TestCase):

    def setUp(self):
        self.address = "via Luigi Gastinelli 118, Rome, Italy"
        self.test_place = PoliticalPlace(
            address=self.address)
        self.test_place_wrong_addr = PoliticalPlace(
            address="kkkkkkkkkkkkkkkkkkkkkkkkkkkk")

    def test_unicode_str(self):
        test_place = PoliticalPlace.get_or_create_from_address(
            self.address)
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
        self.test_place.geo_type = 'administrative_area_level_1'
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
            self.address)
        self.assertEqual(
            test_place.administrative_area_level_1,
            "Lazio")
        self.assertEqual(
            test_place.country,
            "Italy")

    def test_political_place_get_or_create_from_address_fields_creation2(self):
        test_place = PoliticalPlace.get_or_create_from_address(
            "Praha")
        self.assertEqual(
            test_place.locality,
            "Prague")
        self.assertEqual(
            test_place.country,
            "Czechia")
        self.assertEqual(
            test_place.continent,
            "Europe")

    def test_political_place_get_or_create_from_address_fields_creation3(self):
        test_place = PoliticalPlace.get_or_create_from_address(
            "Av de la Cultura, Cusco, Peru")
        self.assertEqual(
            test_place.locality,
            "Cusco")
        self.assertEqual(
            test_place.country,
            "Peru")
        self.assertEqual(
            test_place.continent,
            "South America")

    @skip
    def test_political_place_get_or_create_from_address_route_street_number(self):
        test_place = PoliticalPlace.get_or_create_from_address(
            "Largo Arquata del Tronto 1, 00156 Roma, Italy")
        test_place.refresh_from_db()
        self.assertEqual(
            test_place.route,
            "Via Arquata del Tronto")
        self.assertEqual(
            test_place.street_number,
            "1")
        self.assertEqual(
            test_place.geo_type,
            "street_address")
        self.assertEqual(
            test_place.types,
            "['street_address']")
        self.assertEqual(
            test_place.country,
            "Italy")

    def test_political_place_get_or_create_from_address_neighborhood(self):
        test_place = PoliticalPlace.get_or_create_from_address(
            "via Luigi Gastinelli 118, Rome")
        test_place.refresh_from_db()
        self.assertEqual(
            test_place.administrative_area_level_4,
            "")
        self.assertEqual(
            test_place.neighborhood,
            "Zona IX Acqua Vergine")
        self.assertEqual(
            test_place.route,
            "Via Luigi Gastinelli")
        self.assertEqual(
            test_place.street_number,
            "118")
        self.assertEqual(
            test_place.geo_type,
            "street_address")

    def test_political_place_get_or_create_from_address_no_country(self):
        test_place = PoliticalPlace.get_or_create_from_address(
            "Gaza")
        test_place.refresh_from_db()
        self.assertEqual(
            test_place.geo_type,
            "administrative_area_level_1")
        self.assertEqual(
            test_place.types,
            "['administrative_area_level_1', 'political']")
        self.assertEqual(
            test_place.country,
            "")

    def test_political_place_get_or_create_from_address_items_creation(self):
        test_place = PoliticalPlace.get_or_create_from_address(
            self.address)
        self.assertEqual(
            test_place.administrative_area_level_1_item.long_name,
            "Lazio")
        self.assertEqual(
            test_place.country_item.short_name,
            "IT")

    def test_political_place_get_or_create_from_address_url_parent(self):
        test_place = PoliticalPlace.get_or_create_from_address(
            "Montesacro, Rome")
        map_item_italy = MapItem.objects.get(
            long_name__iexact='Italy',
            geo_type__iexact='country')
        map_item_lazio = MapItem.objects.get(
            long_name__iexact='Lazio',
            geo_type__iexact='administrative_area_level_1')
        map_item_rome_area3 = MapItem.objects.get(
            long_name__icontains='Rome',
            geo_type__iexact='administrative_area_level_3')
        map_item_roma = MapItem.objects.get(
            long_name__iexact='Rome',
            geo_type__iexact='locality')
        self.assertEqual(
            test_place.administrative_area_level_1_item.relative_url,
            "/europe/it/lazio/{}".format(map_item_lazio.pk))
        self.assertEqual(
            test_place.administrative_area_level_1_item.parent,
            map_item_italy)
        self.assertEqual(
            test_place.locality_item.relative_url,
            "/europe/it/lazio/rm/rome/rome/{}".format(
                map_item_roma.pk))
        self.assertEqual(
            test_place.locality_item.parent,
            map_item_rome_area3)

    def test_political_place_process_address_wrong(self):
        with self.assertRaises(NoResultsException):
            PoliticalPlace.get_or_create_from_address(
                self.test_place_wrong_addr.address)

    def test_political_place_get_or_create_from_address_self_item(self):
        colosseo = PoliticalPlace.get_or_create_from_address(
            "Colosseo, Rome")
        self.assertEqual(colosseo.country_item.short_name, "IT")
        self.assertEqual(colosseo.route, "Piazza del Colosseo")
        self.assertEqual(colosseo.street_number, "1")
        self.assertEqual(colosseo.administrative_area_level_2_item.short_name, "RM")
        self.assertEqual(colosseo.sublocality_item.short_name, "Municipio I")
        self.assertEqual(
            colosseo.self_item.short_name,
            "Piazza del Colosseo, 1, 00184 Roma RM, Italy")

    def test_political_place_get_or_create_from_address_gmaps_bug_roviano(self):
        """ Gmaps latlng only returns the street address result, missing all the
        other components."""
        test_place = PoliticalPlace.get_or_create_from_address(
            "Piazza della Repubblica, 00027 Roviano RM")
        self.assertEqual(
            test_place.locality,
            "Roviano")
        self.assertEqual(
            test_place.locality_item.error_log,
            # "Geographical type locality not found in results ['administrative_area_level_3', 'political']")
            "")
        self.assertEqual(
            test_place.country,
            "Italy")
        self.assertEqual(
            test_place.country_item.error_log,
            "")
        self.assertEqual(
            test_place.continent,
            "Europe")

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

    def test_refresh_data(self):
        self.test_place.refresh_data()
        self.assertEqual(
            self.test_place.country_item.short_name, "IT")

    def test_refresh_data_place_id(self):
        self.test_place.place_id = "ChIJu46S-ZZhLxMROG5lkwZ3D7k"
        self.test_place.save()
        self.test_place.refresh_data()
        self.assertEqual(
            self.test_place.country_item.short_name, "IT")


class MapItemModelTest(TestCase):

    def setUp(self):
        self.test_item = MapItem.update_or_create_from_address(
            "Lazio, Italy", 'administrative_area_level_1')

    def test_unicode_str(self):
        self.assertEqual(
            str(self.test_item),
            "Lazio(administrative_area_level_1)")

    def test_get_or_create_from_place_id_create(self):
        place_id = "ChIJNWU6NebuJBMRKYWj8WSQSm8"
        map_item = MapItem.update_or_create_from_place_id(place_id)
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
            MapItem.update_or_create_from_place_id(place_id)

    def test_get_or_create_from_address_create(self):
        address = "Lazio, Italy"
        map_item = MapItem.update_or_create_from_address(
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
            MapItem.update_or_create_from_address(
                address, 'administrative_area_level_1')

    def test_get_or_create_from_address_wrong_geo_type(self):
        address = "Lazio, Italy"
        # with self.assertRaises(GeoTypeException):
        #    MapItem.update_or_create_from_address(
        #        address, 'country')
        map_item = MapItem.update_or_create_from_address(
            address, 'country')
        self.assertEqual(
            map_item.error_log,
            "Geographical type country not found in results ['administrative_area_level_1', 'political']"
        )

    def test_get_or_create_from_address_get(self):
        self.assertEqual(1, MapItem.objects.count())
        address = "Calabria, Italy"
        MapItem.update_or_create_from_address(
            address, 'administrative_area_level_1')
        self.assertEqual(2, MapItem.objects.count())
        MapItem.update_or_create_from_address(
            address, 'administrative_area_level_1')
        self.assertEqual(2, MapItem.objects.count())

    def test_get_or_create_from_address_africa(self):
        address = "Kayuma, CD"
        map_item = MapItem.update_or_create_from_address(
            address, 'locality')
        self.assertEqual(map_item.long_name, "Kayuma")
        self.assertEqual(map_item.short_name, "Kayuma")
        self.assertEqual(map_item.geocode, "-9.383333,21.833333")
        self.assertEqual(
            map_item.place_id,
            'ChIJ4_CniEcdKxoRb3-I6gCh7II')

    def test_get_or_create_from_address_america(self):
        address = "Dosquebradas, Pereira"
        map_item = MapItem.update_or_create_from_address(
            address, 'locality')
        self.assertEqual(map_item.long_name, "Dosquebradas")
        self.assertEqual(map_item.short_name, "Dosquebradas")
        self.assertEqual(map_item.geocode, "4.8318256,-75.68056779999999")
        self.assertEqual(
            map_item.place_id,
            'ChIJhyRrTd-AOI4ReAs5SWb4f5s')

    def test_get_or_create_from_address_asia(self):
        address = "Tokachi District, Japan"
        map_item = MapItem.update_or_create_from_address(
            address, 'locality')
        self.assertEqual(map_item.long_name, "Tokachi District")
        self.assertEqual(map_item.short_name, "Tokachi District")
        self.assertEqual(map_item.geocode, "42.913886,143.6932779")
        self.assertEqual(
            map_item.place_id,
            'ChIJF1BfXpK2c18R4BivzcAmO9M')

    def test_get_or_create_from_address_europe(self):
        address = "Hordaland, Norway"
        map_item = MapItem.update_or_create_from_address(
            address, 'administrative_area_level_1')
        self.assertEqual(map_item.long_name, "Hordaland")
        self.assertEqual(map_item.short_name, "Hordaland")
        self.assertEqual(map_item.geocode, "60.2733674,5.7220194")
        self.assertEqual(
            map_item.place_id,
            'ChIJU9YJbagwPEYR0ByzKCZ3AQM')

    def test_get_or_create_from_address_oceania(self):
        address = "Tonga"
        map_item = MapItem.update_or_create_from_address(
            address, 'country')
        self.assertEqual(map_item.long_name, "Tonga")
        self.assertEqual(map_item.short_name, "TO")
        self.assertEqual(map_item.geocode, "-21.178986,-175.198242")
        self.assertEqual(
            map_item.place_id,
            'ChIJHdCfu0S2k3ERqeJexcrMbfM')

    def test_geometry_properties(self):
        # maxDiff = None
        address = "Thailandia"
        map_item = MapItem.update_or_create_from_address(
            address, 'country')
        self.assertEqual(map_item.long_name, "Thailand")
        self.assertEqual(map_item.short_name, "TH")
        self.assertEqual(map_item.geocode, "15.870032,100.992541")
        self.assertEqual(
            map_item.place_id, 'ChIJsU1CR_eNTTARAuhXB4gs154')
        self.assertEqual(
            map_item.geometry_bounds(False), {
                'northeast': {'lat': 20.465143, 'lng': 105.636812},
                'southwest': {'lat': 5.613038, 'lng': 97.343396}
            })
        self.assertEqual(
            json.loads(map_item.geometry_bounds()), {
                'northeast': {'lat': 20.465143, 'lng': 105.636812},
                'southwest': {'lat': 5.613038, 'lng': 97.343396}
            })
        self.assertEqual(
            map_item.geometry_viewport(False), {
                'northeast': {'lat': 20.465143, 'lng': 105.636812},
                'southwest': {'lat': 5.613038, 'lng': 97.343396}
            })
        self.assertEqual(
            json.loads(map_item.geometry_viewport()), {
                'northeast': {'lat': 20.465143, 'lng': 105.636812},
                'southwest': {'lat': 5.613038, 'lng': 97.343396}
            })
