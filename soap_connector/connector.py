import logging
import operator
import math
from typing import List, Optional

from zeep.client import Client
from zeep.wsdl.definitions import Service, Port

from rest_framework.reverse import reverse

from soap_connector.serializers import ClientSerializer
from soap_connector.api.base import BaseAPIView

logger = logging.getLogger(__name__)


def to_number(s: str) -> int:
    """
    Transform 's' parameter into number and returns it.

    :param s:
    :return:
    """
    return int.from_bytes(s.encode(), 'little')


def from_number(n: int) -> str:
    """
    Transform 'n' parameter into string and returns it.

    :param n:
    :return:
    """
    return n.to_bytes(math.ceil(n.bit_length() / 8), 'little').decode()


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


class Connector(object):
    """

    """

    def __init__(self, client: dict, **kwargs):
        """

        :param kwargs:
        """
        fields = {
            key: value for key, value in client.items()
            if key in ClientSerializer.Meta.fields
        }
        self.client = Client(**fields)
        self.client_pk = client['pk']
        self.context = kwargs['context']

    @classmethod
    def from_view(cls, view: BaseAPIView) -> "Connector":
        """

        :param view:
        :return:
        """
        assert issubclass(view.object_class, Client), (
                "'%s' needs that view context be a Client object "
                "class in order to retrieve serialized client data "
                "from cache."
                % cls.__name__)
        context = view.get_serializer_context()
        pk = view.kwargs['pk']
        client = view.cache[pk]

        return cls(client, context=context)

    @property
    def prefixes(self):
        """

        :return:
        """
        object_list = []

        for data in self.client.wsdl.types.prefix_map.items():
            pk = id(data[0])
            url = reverse(
                f'soap_connector:client_prefix_detail',
                kwargs={'pk': self.client_pk, 'prefix_pk': pk},
                request=self.context['request'])
            object_list.append({
                'pk': pk,
                'prefix': data[0],
                'namespace': data[1],
                'url': url})

        return object_list

    @property
    def global_elements(self):
        """

        :return:
        """
        elements = self.client.wsdl.types.elements
        object_list = []

        for obj in sorted(elements, key=lambda k: k.qname):
            element = obj.signature(schema=self.client.wsdl.types)
            if element:
                pk = id(element)
                url = reverse(
                    f'soap_connector:client_global_type_detail',
                    kwargs={'pk': self.client_pk, 'type_pk': pk},
                    request=self.context['request'])
                object_list.append({'pk': pk, 'global_element': element, 'url': url})

        return object_list

    @property
    def global_types(self):
        """

        :return:
        """
        object_list = []
        for type_obj in sorted(
                self.client.wsdl.types.types,
                key=lambda k: k.qname or ''):
            signature = type_obj.signature(schema=self.client.wsdl.types)
            if signature:
                pk = id(signature)
                url = reverse(
                    f'soap_connector:client_global_type_detail',
                    kwargs={'pk': self.client_pk, 'type_pk': pk},
                    request=self.context['request'])
                object_list.append({'pk': pk, 'type': signature, 'url': url})

        return object_list

    @property
    def bindings(self):
        """

        :return:
        """
        object_list = []
        for binding_obj in sorted(
                self.client.wsdl.bindings.values(),
                key=lambda k: str(k)):
            pk = id(binding_obj.name)
            url = reverse(
                f'soap_connector:client_binding_detail',
                kwargs={'pk': self.client_pk, 'binding_pk': pk},
                request=self.context['request'])
            object_list.append({
                'pk': pk,
                'class': binding_obj.__class__.__name__,
                'name': str(binding_obj.name),
                'port_name': str(binding_obj.port_name),
                'url': url
            })

        return object_list

    @property
    def services(self):
        """

        :return:
        """
        object_list = []
        for service in self.client.wsdl.services.values():
            pk = service.name
            url = reverse(
                f'soap_connector:client_service_detail',
                kwargs={'pk': self.client_pk, 'service_pk': pk},
                request=self.context['request'])
            object_list.append({
                'pk': pk,
                'service': service.name,
                'ports': self.ports(service),
                'url': url
            })

        return object_list

    def ports(self, service: Service):
        """

        :return:
        """
        object_list = []
        for port in service.ports.values():
            pk = port.name
            url = reverse(
                f'soap_connector:client_port_detail',
                kwargs={'pk': self.client_pk, 'service_pk': service.name, 'port_pk': pk},
                request=self.context['request'])
            object_list.append({
                'pk': pk,
                'port': port.name,
                'operations': self.operations(service, port),
                'url': url
            })

        return object_list

    def operations(self, service: Service, port: Port):
        """

        :return:
        """
        object_list = []
        operations = sorted(
            port.binding._operations.values(),
            key=operator.attrgetter('name')
        )
        for operation in operations:
            pk = operation.name
            url = reverse(
                f'soap_connector:client_operation_detail',
                kwargs={
                    'pk': self.client_pk,
                    'service_pk': service.name,
                    'port_pk': port.name,
                    'operation_pk': pk
                },
                request=self.context['request'])
            object_list.append({'pk': pk, 'operation': operation.name, 'url': url})

        return object_list
