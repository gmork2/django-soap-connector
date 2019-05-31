from typing import List, Optional

from rest_framework import serializers

from zeep.client import Client
from zeep.wsdl.definitions import Service, Port, Operation
from zeep.wsdl.messages.soap import SoapMessage

from soap_connector.connector import Connector


def parser(parts: Optional[List[str]] = ()):
    """
    Returns a parser signature.

    :param parts:
    :return:
    """
    for part in parts:
        params = part.split(', ')
        for param in params:
            qname, _type = param.split(': ')
            yield qname, _type


def signature(soap_message: SoapMessage):
    """

    :param soap_message:
    :return:
    """
    if not soap_message.envelope:
        return None

    if soap_message.body:
        parts = [soap_message.body.type.signature(schema=soap_message.wsdl.types, standalone=False)]
    else:
        parts = []

    return parts


class ConnectorMixin(object):
    """

    """
    @property
    def connector(self):
        """

        :return:
        """
        view = self.context['view']

        with view.context(Client):
            return Connector.from_view(view)

    def get_name(self, cls, pk_name):
        """

        :param cls:
        :param pk_name:
        :return:
        """
        view = self.context['view']

        with view.context(cls):
            pk = view.kwargs[pk_name]
            return view.cache[pk]['name']

    @property
    def service(self):
        """

        :return:
        """
        service_name = self.get_name(Service, 'service_pk')
        client = self.connector.client

        return client.wsdl.services[service_name]

    @property
    def port(self):
        """

        :return:
        """
        port_name = self.get_name(Port, 'port_pk')
        return self.service.ports[port_name]

    @property
    def operation(self):
        """

        :return:
        """
        operation_name = self.get_name(Operation, 'operation_pk')
        ops = getattr(self.port.binding, '_operations')

        return ops[operation_name]


class OperationSerializer(serializers.Serializer,
                          ConnectorMixin):
    """

    """
    pass
