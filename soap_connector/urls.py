from django.urls import path

from soap_connector import api


urlpatterns = [
    path('', api.root),
    path('settings/<int:pk>/', api.settings, name='settings_detail'),
    path('settings/', api.settings, name='settings_list'),
    path('client/<int:pk>/binding/<int:binding_pk>/', api.binding, name='client_binding_detail'),
    path('client/<int:pk>/binding/', api.binding, name='client_binding_list'),
    path('client/<int:pk>/prefix/<int:prefix_pk>/', api.prefix, name='client_prefix_detail'),
    path('client/<int:pk>/prefix/', api.prefix, name='client_prefix_list'),
    path('client/<int:pk>/element/<int:element_pk>/', api.global_element, name='client_global_element_detail'),
    path('client/<int:pk>/element/', api.global_element, name='client_global_element_list'),
    path('client/<int:pk>/type/<int:type_pk>/', api.global_type, name='client_global_type_detail'),
    path('client/<int:pk>/type/', api.global_type, name='client_global_type_list'),
    path('client/<int:pk>/', api.client, name='client_detail'),
    path('client/', api.client, name='client_list'),
    path('signature/<int:pk>/', api.signature, name='signature_detail'),
    path('signature/', api.signature, name='signature_list'),
    path('username_token/<int:pk>/', api.username_token, name='username_token_detail'),
    path('username_token/', api.username_token, name='username_token_list'),
]
