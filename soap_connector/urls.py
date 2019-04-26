from django.urls import path

from soap_connector import api


urlpatterns = [
    path('', api.root),
    path('settings/<int:pk>/', api.settings, name='settings_detail'),
    path('settings/', api.settings, name='settings_list'),
    path('signature/<int:pk>/', api.signature, name='signature_detail'),
    path('signature/', api.signature, name='signature_list'),
    path('username_token/<int:pk>/', api.username_token, name='username_token_detail'),
    path('username_token/', api.username_token, name='username_token_list'),
]
