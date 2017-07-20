from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from .backends import Client
from .exceptions import (
    NoResultsException, ExistingPlaceID)  # GeoTypeException,
from .utils import country_to_continent
from collections import OrderedDict
import json


POLITICAL_TYPES = [
    'continent',
    'country',
    'administrative_area_level_1',
    'administrative_area_level_2',
    'administrative_area_level_3',
    'administrative_area_level_4',
    'administrative_area_level_5',
    'locality',
    'ward',
    'sublocality',
    'neighborhood',
]

DETAIL_TYPES = POLITICAL_TYPES + [
    'route',
    'street_number',
    'postal_code',
]


def _get_main_type(types):
    for t in POLITICAL_TYPES:
        if t in types:
            return t
    try:
        return types[0]
    except IndexError:
        return ""


class MapItem(models.Model):
    place_id = models.CharField(unique=True, max_length=255)
    long_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, blank=True)
    geo_type = models.CharField(max_length=100)
    types = models.CharField(max_length=255)
    response_json = models.TextField()
    geocode = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200)
    url = models.CharField(max_length=255, blank=True)
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL)
    error_log = models.TextField(blank=True)

    @classmethod
    def _update_or_create_item(
            cls, geocode_result, types_list, url, parent, error_log=""):
        address_components = geocode_result['address_components'][0]
        location = geocode_result['geometry']['location']
        slug = slugify(address_components['short_name'])[:200]
        if slug == "":
            slug = slugify(address_components['long_name'])[:200]
        mapitem, _ = cls.objects.update_or_create(
            place_id=geocode_result['place_id'],
            defaults={
                'long_name': address_components['long_name'],
                'short_name': address_components['short_name'],
                'geo_type': _get_main_type(types_list),
                'types': ",".join(types_list),
                'response_json': json.dumps(geocode_result),
                'geocode': "{},{}".format(location['lat'], location['lng']),
                'slug': slug,
                'url': "{}/{}".format(url, slug),
                'parent': parent,
                'error_log': error_log,
            })
        return mapitem

    @classmethod
    def update_or_create_from_political_place(
            cls, place_id, name, geo_type, types, response_json,
            geocode, url, parent, error_log=""):
        slug = slugify(name)[:200]
        mapitem, _ = cls.objects.update_or_create(
            place_id=place_id,
            defaults={
                'long_name': name,
                'short_name': name,
                'geo_type': geo_type,
                'types': types,
                'response_json': response_json,
                'geocode': geocode,
                'slug': slug,
                'url': "{}/{}".format(url, slug),
                'parent': parent,
                'error_log': error_log,
            })
        return mapitem

    @classmethod
    def update_or_create_from_place_id(
            cls, place_id, expected_type=None, url='', parent=None):
        """
        geocodes provided place_id and builds the url adding the slug.
        All returned types are stored as comma separated slugs in
        'types' attribute.
        """
        client = Client()
        geocode_result = client.reverse_geocode(place_id)
        # if results, take the first one. No way to let the user
        # choose between different solutions, like in the frontend form
        geocode_result = geocode_result[0]
        types_list = geocode_result['types']
        #if expected_type and expected_type not in types_list:
        #    types_list.append(expected_type)
        return cls._update_or_create_item(geocode_result, types_list, url, parent)

    @classmethod
    def update_or_create_from_address(
            cls, address, geo_type, url='', parent=None):
        """
        geocodes provided address, checks if attended geo_type is
        in results and builds the url adding the slug.
        If geo_type is None, any geo_type will be accepted.
        geo_type is the 'main' type used for geopolitical groups
        and marker-clustering. All returned types are stored as
        comma separated slugs in 'types' attribute.
        """
        client = Client()
        geocode_result = client.geocode(address)
        if geocode_result == []:
            raise NoResultsException("Address Not Found")
        # if results, take the first one. No way to let the user
        # choose between different solutions, like in the frontend form
        geocode_result = geocode_result[0]
        types_list = geocode_result['address_components'][0]['types']
        error_log = ""
        if geo_type not in types_list:
            error_log = "Geographical type {} not found in results {}".format(
                geo_type, types_list)
            #raise GeoTypeException(
            #    "Geographical type {} not found in results {}".format(
            #        geo_type, types_list))
        return cls._update_or_create_item(
            geocode_result, types_list, url, parent, error_log)

    @property
    def relative_url(self):
        return "{}/{}".format(self.url, self.pk)

    def _get_json_attribute(self, nodes):
        try:
            source = json.loads(self.response_json)
        except (ValueError, KeyError):
            return None
        else:
            node = source
            try:
                for n in nodes:
                    node = node[n]
            except KeyError:
                return None
            else:
                return node

    def geometry_bounds(self, json_output=True):
        bounds = self._get_json_attribute(['geometry', 'bounds'])
        if json_output:
            return json.dumps(bounds)
        else:
            return bounds

    def geometry_viewport(self, json_output=True):
        viewport = self._get_json_attribute(['geometry', 'viewport'])
        if json_output:
            return json.dumps(viewport)
        else:
            return viewport

    def __str__(self):
        return "{}({})".format(self.long_name, self.geo_type)

    def __unicode__(self):
        return self.__str__()


class PoliticalPlace(models.Model):

    """
    Geo Types according to google maps standard:
    https://developers.google.com/maps/documentation/geocoding/intro#Types
    The model manages all the 'political' types
    """
    continent = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    administrative_area_level_1 = models.CharField(
        max_length=255, blank=True)
    administrative_area_level_2 = models.CharField(
        max_length=255, blank=True)
    administrative_area_level_3 = models.CharField(
        max_length=255, blank=True)
    administrative_area_level_4 = models.CharField(
        max_length=255, blank=True)
    administrative_area_level_5 = models.CharField(
        max_length=255, blank=True)
    locality = models.CharField(max_length=255, blank=True)
    ward = models.CharField(max_length=255, blank=True)
    sublocality = models.CharField(max_length=255, blank=True)
    neighborhood = models.CharField(max_length=255, blank=True)
    route = models.CharField(max_length=255, blank=True)
    street_number = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    place_id = models.CharField(unique=True, max_length=255)
    geocode = models.CharField(max_length=255, blank=True)
    geo_type = models.CharField(max_length=100, blank=True)
    types = models.CharField(max_length=255, blank=True)
    response_json = models.TextField(blank=True)
    continent_item = models.ForeignKey(
        MapItem, on_delete=models.SET_NULL,
        related_name='politicalplace_continent_set',
        null=True, blank=True)
    country_item = models.ForeignKey(
        MapItem, on_delete=models.SET_NULL,
        related_name='politicalplace_country_set',
        null=True, blank=True)
    administrative_area_level_1_item = models.ForeignKey(
        MapItem, on_delete=models.SET_NULL,
        related_name='politicalplace_aal1_set',
        null=True, blank=True)
    administrative_area_level_2_item = models.ForeignKey(
        MapItem, on_delete=models.SET_NULL,
        related_name='politicalplace_aal2_set',
        null=True, blank=True)
    administrative_area_level_3_item = models.ForeignKey(
        MapItem, on_delete=models.SET_NULL,
        related_name='politicalplace_aal3_set',
        null=True, blank=True)
    administrative_area_level_4_item = models.ForeignKey(
        MapItem, on_delete=models.SET_NULL,
        related_name='politicalplace_aal4_set',
        null=True, blank=True)
    administrative_area_level_5_item = models.ForeignKey(
        MapItem, on_delete=models.SET_NULL,
        related_name='politicalplace_aal5_set',
        null=True, blank=True)
    locality_item = models.ForeignKey(
        MapItem, on_delete=models.SET_NULL,
        related_name='politicalplace_locality_set',
        null=True, blank=True)
    ward_item = models.ForeignKey(
        MapItem, on_delete=models.SET_NULL,
        related_name='politicalplace_ward_set',
        null=True, blank=True)
    sublocality_item = models.ForeignKey(
        MapItem, on_delete=models.SET_NULL,
        related_name='politicalplace_sublocality_set',
        null=True, blank=True)
    neighborhood_item = models.ForeignKey(
        MapItem, on_delete=models.SET_NULL,
        related_name='politicalplace_neighborhood_set',
        null=True, blank=True)
    self_item = models.ForeignKey(
        MapItem, on_delete=models.SET_NULL,
        related_name='politicalplace_self_set',
        null=True, blank=True)

    @property
    def lat(self):
        if self.geocode:
            return self.geocode.split(",")[0]
        return None

    @property
    def lng(self):
        if self.geocode:
            return self.geocode.split(",")[1]
        return None

    def _create_map_items(self, client, lat, lng):
        """Create map_items"""

        if self.geo_type and self.geo_type in POLITICAL_TYPES:
            edge_type = self.geo_type
        else:
            edge_type = None
        # list of results from latlng reverse geocoding
        latlng_results = client.reverse_geocode((lat, lng))
        latlng_components = OrderedDict(
            [(_get_main_type(x['types']), x) for
             x in latlng_results[::-1]])
        parent = None
        url = ''
        for component in POLITICAL_TYPES:
            try:
                # try to get component object
                map_component = latlng_components[component]
            except KeyError:
                # if it doesn't exist (ex. Continent), try to add it using
                # the saved string address
                if getattr(self, component) not in ["", None]:
                    map_item = MapItem.update_or_create_from_address(
                        getattr(self, component), component,
                        url=url, parent=parent)
                else:
                    if component == edge_type:
                        return
                    continue
            else:
                # otherwise you can use the place_id, that's better
                map_item = MapItem.update_or_create_from_place_id(
                    map_component['place_id'], expected_type=component,
                    url=url, parent=parent)
                if getattr(self, component) in ["", None]:
                    setattr(self, component, map_item.long_name)

            # finally set the item element and update url and parent
            setattr(self, "{}_item".format(component), map_item)
            if component == edge_type:
                return
            url = map_item.url
            parent = map_item
        if 'political' not in self.types:
            self.self_item = MapItem.update_or_create_from_political_place(
                self.place_id, self.address, self.geo_type, self.types,
                self.response_json, self.geocode, url, parent)

    def refresh_data(self):
        """
        if for any reason your PoliticalPlace object has only address and
        place_id, or you need to refresh geographic data from the source app
        (googlemaps, etc.), you can perform this action.
        This will work even only with the address (python object not already
        db object)
        """
        if self.place_id:
            place = self._geocode_item(self.place_id, True)
        else:
            place = self._geocode_item(self.address)
        place.save()

    def _process_address(self):
        return self._geocode_item(self.address, provide_new=True)

    def _geocode_item(self, to_geocode, reverse=False, provide_new=False):
        """
        Use this method to process a Place with only the address provided
        """
        client = Client()
        if reverse:
            geocode_result = client.reverse_geocode(to_geocode)
        else:
            geocode_result = client.geocode(to_geocode)
        if geocode_result == []:
            raise NoResultsException("Address Not Found")
        # if results, take the first one. No way to let the user
        # choose between different solutions, like in the frontend form
        geocode_result = geocode_result[0]
        address_components = geocode_result['address_components']
        location = geocode_result['geometry']['location']

        self.address = geocode_result['formatted_address']
        self.place_id = geocode_result['place_id']
        try:
            existing_item = self.__class__.objects.exclude(pk=self.pk).get(
                place_id=self.place_id)
        except self.__class__.DoesNotExist:
            pass
        else:
            if not provide_new:
                raise ExistingPlaceID(
                    "Place with place_id {} already exists.".format(
                        self.place_id))
            return existing_item
        self.geocode = "{},{}".format(location['lat'], location['lng'])
        self.geo_type = _get_main_type(geocode_result['types'])
        self.types = geocode_result['types'] or ""
        self.response_json = json.dumps(geocode_result)
        for component in address_components[::-1]:
            for t in DETAIL_TYPES:
                if t in component['types']:
                    setattr(self, t, component['long_name'])
                elif not getattr(self, t):
                    setattr(self, t, "")
        self.continent = country_to_continent(self.country)
        if not self.continent:
            self.continent = ""
        self._create_map_items(client, location['lat'], location['lng'])
        return self

    @classmethod
    def get_or_create_from_address(cls, address):
        """
        Use this method to get or create a PoliticalPlace when only
        the address is given (for example using it in the backend only)
        """
        place = cls(address=address)
        place = place._process_address()
        place.save()
        return place

    def link_map_items(self):
        """
        Use this method when your object has all the static geograpghic
        informations filled by frontend
        """
        client = Client()
        self.continent = country_to_continent(self.country)
        if not self.continent:
            self.continent = ""
        self._create_map_items(client, self.lat, self.lng)
        self.save()

    def __str__(self):
        return self.address

    def __unicode__(self):
        return self.__str__()
