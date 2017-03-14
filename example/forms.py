from django.forms import ModelForm
from .models import MyLocation


class MyLocationForm(ModelForm):

    class Meta:
        model = MyLocation
        fields = '__all__'
