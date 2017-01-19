from django.db import models
from django.template.defaultfilters import slugify
from .backends import Client
from .exceptions import NoResultsException, GeoTypeException
from .utils import country_to_continent
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
]


class MapItem(models.Model):
    place_id = models.CharField(max_length=255)
    long_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, blank=True)
    geo_type = models.CharField(max_length=100)
    types = models.CharField(max_length=255)
    response_json = models.TextField()
    geocode = models.CharField(max_length=255)
    slug = models.SlugField()
    #use_viewport = models.BooleanField(default=True)
    url = models.CharField(max_length=255, blank=True)
    #custom_zoom = models.PositiveSmallIntegerField(
    #    blank=True, null=True, choices=[(x, x) for x in range(1, 22)])

    @classmethod
    def get_or_create_from_place_id(cls, place_id, url=''):
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
        address_components = geocode_result['address_components'][0]
        location = geocode_result['geometry']['location']
        slug = slugify(address_components['long_name'])
        mapitem, created = cls.objects.get_or_create(
            place_id=geocode_result['place_id'],
            defaults={
                'long_name': address_components['long_name'],
                'short_name': address_components['short_name'],
                'geo_type': types_list[0],
                'types': ",".join(types_list),
                'response_json': json.dumps(geocode_result),
                'geocode': "{},{}".format(location['lat'], location['lng']),
                'slug': slug,
                'url': "{}/{}".format(url, slug)
            })
        return mapitem

    @classmethod
    def get_or_create_from_address(cls, address, geo_type, url=''):
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
        if geo_type not in types_list:
            raise GeoTypeException(
                "Geographical type {} not found in results {}".format(
                    geo_type, types_list))
        address_components = geocode_result['address_components'][0]
        location = geocode_result['geometry']['location']
        slug = slugify(address_components['long_name'])
        mapitem, created = cls.objects.get_or_create(
            place_id=geocode_result['place_id'],
            defaults={
                'long_name': address_components['long_name'],
                'short_name': address_components['short_name'],
                'geo_type': geo_type,
                'types': ",".join(types_list),
                'response_json': json.dumps(geocode_result),
                'geocode': "{},{}".format(location['lat'], location['lng']),
                'slug': slug,
                'url': "{}/{}".format(url, slug)
            })
        return mapitem


class PoliticalPlace(models.Model):

    """
    Geo Types according to google maps standard:
    https://developers.google.com/maps/documentation/geocoding/intro#Types
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
    address = models.CharField(max_length=255)
    #address = GmapsField(plugin_options={
    #    'geocode_field': 'geocode', 'type_field': 'geo_type',
    #    'allowed_types': ALLOWED_TYPES},
    #    select2_options={'width': '300px'},
    #    help_text=(u"Type the address you're looking for and click "
    #               u"on the red marker to select it."))
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

    @staticmethod
    def _get_main_type(types):
        for t in POLITICAL_TYPES:
            if t in types:
                return t
        return types[0]

    def _create_map_items(self, client, lat, lng):
        # self already has administrative levels filled
        # run reverse geocoding
        reverse_results = client.reverse_geocode((lat, lng))
        # first set the continent, usually not a political place
        if self.continent not in (None, ""):
            continent_item = MapItem.get_or_create_from_address(
                self.continent, 'continent')
            self.continent_item = continent_item
        # then, for each result
        for item in reverse_results:
            # if its related field is not empty
            t = self._get_main_type(item['types'])
            try:
                if getattr(self, t) not in (None, ""):
                    # get_or_create map item from place_id
                    map_item = MapItem.get_or_create_from_place_id(
                        item['place_id'])
                    setattr(self, "{}_item".format(t), map_item)
            except AttributeError:
                pass  # type is not political

    def process_address(self):
        client = Client()
        geocode_result = client.geocode(self.address)
        if geocode_result == []:
            raise NoResultsException("Address Not Found")
        # if results, take the first one. No way to let the user
        # choose between different solutions, like in the frontend form
        geocode_result = geocode_result[0]
        address_components = geocode_result['address_components']
        location = geocode_result['geometry']['location']

        self.address = geocode_result['formatted_address']
        self.place_id = geocode_result['place_id']
        self.geocode = "{},{}".format(location['lat'], location['lng'])
        self.geo_type = self._get_main_type(geocode_result['types'])
        self.types = geocode_result['types']
        self.response_json = json.dumps(geocode_result)
        self.continent = country_to_continent(self.country)
        for component in address_components[::-1]:
            for t in POLITICAL_TYPES:
                if t in component['types']:
                    setattr(self, t, component['long_name'])
                else:
                    setattr(self, t, "")

        self._create_map_items(client, location['lat'], location['lng'])
        self.save()

    #def save(self, *args, **kwargs):
    #    super(PoliticalPlace, self).save(*args, **kwargs)
