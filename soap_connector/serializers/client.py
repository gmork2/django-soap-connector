from rest_framework import serializers

from .base import BaseSerializer
from soap_connector.fields import HyperlinkedField


class ClientSerializer(BaseSerializer):
    """

    """
    wsdl = serializers.URLField()
    # wsse = serializers.ForeignKey()
    transport = None
    service_name = serializers.CharField(required=False)
    port_name = serializers.CharField(required=False)
    # settings = SettingsSerializer(required=False)
    settings = serializers.IntegerField(min_value=1, required=False)
    url = HyperlinkedField(view_name='soap_connector:client_detail')
    prefixes = HyperlinkedField(view_name='soap_connector:client_prefix_list')

    class Meta:
        fields = ['wsdl', 'service_name', 'port_name', 'settings']
