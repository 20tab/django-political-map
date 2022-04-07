from __future__ import unicode_literals

from django.conf import settings
import importlib


Client = getattr(
    importlib.import_module(
        "{}.{}".format(
            'politicalplaces.backends',
            settings.POLITICAL_MAP_BACKEND)),
    'Client')
