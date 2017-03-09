from django.db import models
from politicalplaces.fields import PlaceField


class MyLocation(models.Model):
    place = PlaceField(
        on_delete=models.SET_NULL,
        null=True, blank=True)


class MyLocationMultiPlace(models.Model):
    place1 = PlaceField(
        on_delete=models.SET_NULL,
        related_name="mylocation_places1",
        null=True, blank=True)
    place2 = PlaceField(
        on_delete=models.SET_NULL,
        related_name="mylocation_places2",
        null=True, blank=True)
