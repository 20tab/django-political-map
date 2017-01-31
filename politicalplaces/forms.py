#from django import forms
#from .models import PoliticalPlace
#from .widgets import PlaceWidget
#
#
#class PoliticalPlaceForm(forms.ModelForm):
#
#    def save(self, commit=True):
#        fake = super(PoliticalPlaceForm, self).save(commit=False)
#        place = self.instance.get_or_create_from_address(self.instance.address)
#        print("hhhhhhhhhhhhhhhhhhhhhh")
#        print(place)
#        print(place.country)
#        print(place.country_item)
#        return place
#
#    class Meta:
#        model = PoliticalPlace
#        exclude = []
#        widgets = {'address': PlaceWidget}
