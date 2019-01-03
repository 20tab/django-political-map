from django.db import models
from politicalplaces.fields import PlaceField


class MyLocation(models.Model):
    place = PlaceField(
        on_delete=models.SET_NULL,
        null=True, blank=True)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return str(self.place)


class MyLocationMultiPlace(models.Model):
    place1 = PlaceField(
        on_delete=models.SET_NULL,
        related_name="mylocation_places1",
        null=True, blank=True)
    place2 = PlaceField(
        on_delete=models.SET_NULL,
        related_name="mylocation_places2",
        null=True, blank=True)


class MyLocationInlineTest(MyLocation):

    class Meta:
        proxy = True


class MyLocationInlinePlace(models.Model):
    parent_location = models.ForeignKey(MyLocation, on_delete=models.CASCADE)
    place = PlaceField(
        on_delete=models.SET_NULL,
        null=True, blank=True)


class MyLocationInlineNotPlace(models.Model):
    parent_location = models.ForeignKey(MyLocation, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)


class MyLocationComplex(models.Model):
    mandatory_charfield = models.CharField(max_length=200)
    place = PlaceField(
        on_delete=models.SET_NULL,
        null=True, blank=True)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return str(self.place)
