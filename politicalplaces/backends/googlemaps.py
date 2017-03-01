from __future__ import absolute_import

from googlemaps import Client as GmapsClient
from django.conf import settings


class Client(GmapsClient):

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(
            key=settings.GOOGLE_API_KEY)

    def geocode(self, address=None, components=None,
                bounds=None, region=None,
                language=settings.POLITICAL_MAP_LANGUAGE_CODE):
        return super(Client, self).geocode(
            address, components, bounds, region, language)
