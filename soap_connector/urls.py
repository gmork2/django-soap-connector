from django.urls import path

from soap_connector import api


urlpatterns = [
    path('', api.root),
]
