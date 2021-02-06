from django.urls import path

from soap_connector import api


urlpatterns = [
    path('', api.root, name='root'),
    path('registry/', api.registry, name='registry_list'),
    path('settings/<int:settings_pk>/', api.settings, name='settings_detail'),
    path('settings/', api.settings, name='settings_list'),
    path('client/<int:client_pk>/service/<slug:service_pk>/<slug:port_pk>/<slug:operation_pk>',
         api.operation, name='client_operation_detail'),
    path('client/<int:client_pk>/service/<slug:service_pk>/<slug:port_pk>/', api.port, name='client_port_detail'),
    path('client/<int:client_pk>/service/<slug:service_pk>/', api.service, name='client_service_detail'),
    path('client/<int:client_pk>/service/', api.service, name='client_service_list'),
    path('client/<int:client_pk>/binding/<slug:binding_pk>/', api.binding, name='client_binding_detail'),
    path('client/<int:client_pk>/binding/', api.binding, name='client_binding_list'),
    path('client/<int:client_pk>/prefix/<slug:prefix_pk>/', api.prefix, name='client_prefix_detail'),
    path('client/<int:client_pk>/prefix/', api.prefix, name='client_prefix_list'),
    path('client/<int:client_pk>/element/<slug:element_pk>/', api.global_element, name='client_global_element_detail'),
    path('client/<int:client_pk>/element/', api.global_element, name='client_global_element_list'),
    path('client/<int:client_pk>/type/<slug:type_pk>/', api.global_type, name='client_global_type_detail'),
    path('client/<int:client_pk>/type/', api.global_type, name='client_global_type_list'),
    path('client/<int:client_pk>/', api.client, name='client_detail'),
    path('client/', api.client, name='client_list'),
    path('signature/<int:signature_pk>/', api.signature, name='signature_detail'),
    path('signature/', api.signature, name='signature_list'),
    path('username_token/<int:username_token_pk>/', api.username_token, name='username_token_detail'),
    path('username_token/', api.username_token, name='username_token_list'),
]
