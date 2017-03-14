Django Political Map
====================

Django application to store geolocalized places and organize them
according to political hierarchy.

Features:
- store your geographic data in a single model
- provide address and process it to automatically fill all geo informations
- using the provided form you can choose the place on the map
- and process automatically the location

Installation
------------
This package is under development end needs live testing.
If you want to try it in your project, you can install the
git version:

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
There is one only entry point to the app, that is the **Placefield**
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

Javascript Initialization
--------------------------
Django Political Map as full support for single PlaceField,
multiple PlaceField on the same model and inline models with PlaceField.

The default widget will work on your custom frontend too (just remember to
use {{forms.media}} in your template.

If you need to initialize the library: `politicalplaces.init()`.
The library also supports django inline formsets via the `formset:added` event if using `django.jQuery`,
otherwise you can attach to your custom event the handler 
`politicalplaces.addNewWidget(widgetDOMElement, formsetName)

GMAPS quota limit
-----------------
Using googlemaps as backend, remember there's a quota limit
as described here: https://developers.google.com/maps/documentation/javascript/usage
