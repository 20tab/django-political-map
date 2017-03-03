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
# POLITICAL_MAP_JQUERY_LIB (tested on "https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js")
POLITICAL_MAP_JQUERY_LIB = "yyyyyyyyyyyyyy"
```
  
  - run migrations to update your db **python manage.py migrate**
  
  - manage static files using:
    - django **collectstatic** or  
    - uwsgi **static-map = /static/politicalplaces/=%(lib)/politicalplaces/static/politicalplaces**
    

How to
------
There is one only entry point to the app, that is the **Placefield**
This field is a Foreign Key to PoliticalPlace, so you shoudl use it 
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
