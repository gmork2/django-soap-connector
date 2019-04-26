import logging
import math

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
        return

    @property
    def services(self):
        """

        :return:
        """
        return

    def ports(self, service: Service):
        """

        :return:
        """
        return

    def operations(self, service: Service, port: Port):
        """

        :return:
        """
        return
