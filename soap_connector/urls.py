from django.urls import path

from soap_connector import api


urlpatterns = [
    path('', api.root),
    path('settings/<int:pk>/', api.settings, name='settings_detail'),
    path('settings/', api.settings, name='settings_list'),
]
