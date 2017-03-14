from django.conf.urls import url
from .views import MyLocationCreate

urlpatterns = [
    url(r'^$', MyLocationCreate.as_view(), name='mylocation-create'),
]
