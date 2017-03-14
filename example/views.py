from django.views.generic.edit import CreateView
from .models import MyLocation


class MyLocationCreate(CreateView):
    model = MyLocation
    fields = '__all__'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(MyLocationCreate, self).get_context_data(**kwargs)
        context['locations'] = MyLocation.objects.all()
        return context
