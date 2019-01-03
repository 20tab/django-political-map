[![Build Status](https://travis-ci.org/20tab/django-political-map.svg?branch=master)](https://travis-ci.org/20tab/django-political-map)

Django Political Map
====================

Django application to store geolocalized places and organize them
according to political hierarchy.

Note: this project doesn't require GeoDjango or Gis fields, you should save
geographical data in your own model in order to perform gis queries.

Features:
- store your geographic data in a single model
- provide address and process it to automatically fill all geo informations
- using the provided form you can choose the place on the map
- and process automatically the location

Installation
------------
This package looks stable but it needs more live testing.
If you want to try it in your project, you can pip install it:

  - ```pip install django-political-map```

  or via git:

  - ```pip install git+https://github.com/20tab/django-political-map.git```
  
  - add ```politicalplaces``` in your INSTALLED_APPS
  
  - set mandatory parameters in your settings file:
```python
# BACKEND (googlemaps is the only available backend)
POLITICAL_MAP_BACKEND = 'googlemaps'
# MAP LANGUAGE (en is the only available language)
POLITICAL_MAP_LANGUAGE_CODE = 'en'
# GMAPS (gmaps key is mandatory)
GOOGLE_API_KEY = "xxxxxxxxxxxxxxxx"
```
  
  - run migrations to update your db **python manage.py migrate**
  
  - manage static files using:
    - django **collectstatic** or  
    - uwsgi **static-map = /static/politicalplaces/=%(lib)/politicalplaces/static/politicalplaces**
    

How to
------
There is one only entry point to the app, that is the **Placefield**.
This field is a Foreign Key to PoliticalPlace, so you should use it 
this way:
```python
from django.db import models                                                
from politicalplaces.fields import PlaceField


class MyLocation(models.Model):
    place = PlaceField(
        on_delete=models.SET_NULL,
        null=True, blank=True)
```
PoliticalPlace and MapItem admin are available, but you should never add
these objects directly.

Using PoliticalPlace in the views
---------------------------------
```python
from politicalplaces.models import PoliticalPlace
from .models import MyLocation


loc = MyLocation()
loc.name = "Test Location"
place = PoliticalPlace.get_or_create_from_address(
    address='via Luigi Gastinelli, Rome')
loc.place = place
loc.save()
```

Refresh Data (django command)
-----------------------------
```
(django-political-map) 20tab:django-political-map gabbo$ python manage.py refresh_data --help
usage: manage.py refresh_data [-h] [--version] [-v {0,1,2,3}]
                              [--settings SETTINGS] [--pythonpath PYTHONPATH]
                              [--traceback] [--no-color]
                              [place_id [place_id ...]]

Refresh map data calling the external api

positional arguments:
  place_id              The id list, separeted by space, of the involved
                        PoliticalPlace objects.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.

(django-political-map) 20tab:django-political-map gabbo$ python manage.py refresh_data 2
Refresh data started.
Refreshing data for PoliticalPlace: 2 - Brisbane QLD, Australia
Refresh data completed successfully  for 1 items, 0 errors.

(django-political-map) 20tab:django-political-map gabbo$ python manage.py refresh_data 2 3 4
Refresh data started.
Refreshing data for PoliticalPlace: 2 - Brisbane QLD, Australia
Refreshing data for PoliticalPlace: 3 - Via Luigi Gastinelli, 118, 00132 Roma RM, Italy
Refreshing data for PoliticalPlace: 4 - US-3, United States
Refresh data completed successfully for 3 items, 0 errors.

(django-political-map) 20tab:django-political-map gabbo$ python manage.py refresh_data 2 3 4 -v 0
Refresh data started.
Refresh data completed successfully for 3 items, 0 errors.

(django-political-map) 20tab:django-political-map gabbo$ python manage.py refresh_data
Refresh data started.
Refreshing data for PoliticalPlace: 2 - Brisbane QLD, Australia
Refreshing data for PoliticalPlace: 3 - Via Luigi Gastinelli, 118, 00132 Roma RM, Italy
[...]
Refreshing data for PoliticalPlace: 28 - Čerpadlová 572/5, Vysočany, 190 00 Praha-Praha 9, Czechia
Refresh data completed successfully for 27 items, 0 errors.
```

Javascript Initialization
--------------------------
Django Political Map has full support for admin change_form with
single PlaceField, multiple PlaceField on the same model and
inline models with PlaceField.

The default widget will work on your custom frontend too (just remember to
use {{forms.media}} in your template).

The library also supports django inline formsets via the `formset:added`
event if using `django.jQuery` ("admin/js/vendor/jquery/jquery.js", "admin/js/jquery.init.js"),
otherwise you can attach to your custom event the
`politicalplaces.addNewWidget(widgetDOMElement, formsetName)` handler. 
Example:
```
document.querySelector('button.add-form').addEventListener('click', function() {
  var formsetName = 'the_name_of_the_formset';
  var widgetDOMElement = document.querySelector('.widget');
  politicalplaces.addNewWidget(widgetDOMElement, formsetName);
});
```


GMAPS quota limit
-----------------
Using googlemaps as backend, remember there's a quota limit
as described here: https://developers.google.com/maps/documentation/javascript/usage
