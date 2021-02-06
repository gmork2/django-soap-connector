import logging
from typing import ClassVar

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from zeep.client import Client
from zeep.wsdl.definitions import Binding
from zeep.xsd.types import Type
from zeep.xsd.elements import Element

from soap_connector.serializers import ClientSerializer
from soap_connector.api.base import BaseAPIView
from soap_connector.connector import Connector
from soap_connector.cache import CacheIterator
from soap_connector.exceptions import ConnectorError, CacheError

logger = logging.getLogger(__name__)


class ClientView(BaseAPIView):
    """
    This class defines a CRUD interface for client objects.
    """
    serializer_class = ClientSerializer
    object_class = Client


class ConnectorView(ClientView):
    """
    Class to provide read-only methods to interact with a SOAP
    server through connector.
    """
    source_name: ClassVar[str] = ''

    @property
    def allowed_methods(self):
        """
        The list of HTTP method names that this view will
        accept.

        :return:
        """
        return ['GET']

    def list(self, request: Request, **kwargs) -> Response:
        """
        Concrete view for listing a collection of objects
        from connector.

        :param request:
        :param kwargs:
        :return:
        """
        with self.with_context(Client):
            try:
                connector = Connector.from_view(self)
            except (CacheError, ConnectorError):
                return Response(status=status.HTTP_409_CONFLICT)
            else:
                data = getattr(connector, self.source_name, None)
                if data:
                    self.save(data)
                    return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, **kwargs) -> Response:
        """
        Concrete view for retrieve an object by object_pk_name.

        :param request:
        :param kwargs:
        :return:
        """

        object_pk: int = kwargs.get(self.object_pk_name, None)

        if object_pk is None:
            return self.list(request, **kwargs)
        else:
            data: dict = self.cache[object_pk]
            if data is not None:
                return Response(data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def save_all(self, object_list, cls, lookup=None):
        """
        Iterates on object_list and its recursively nested lists.

        :param object_list: Current object list
        :param cls: Class to which the context belongs
        :param lookup: Indicates the sublists on which to nest
        :return:
        """
        iterator = CacheIterator(object_list, cls, self)

        while True:
            try:
                item = next(iterator)
                if lookup:
                    key, cls = lookup.pop(0)
                    self.save_all(item[key], cls, lookup)

            except StopIteration:
                break

    def save(self, object_list):
        """
        Saves an object list.

        :param object_list:
        :return:
        """
        self.save_all(object_list, Client)


class GlobalTypeView(ConnectorView):
    """
    Class to retrieve information about global types.
    """
    object_class = Type
    source_name: ClassVar[str] = 'global_types'
    object_pk_name: ClassVar[str] = 'type_pk'


class GlobalElementView(ConnectorView):
    """
    Class to retrieve information about elements.
    """
    object_class = Element
    source_name: ClassVar[str] = 'global_elements'
    object_pk_name: ClassVar[str] = 'element_pk'


class PrefixView(ConnectorView):
    """
    Class to retrieve information about prefixes.
    """
    object_class = type('Prefix', (), {})
    source_name: ClassVar[str] = 'prefixes'
    object_pk_name: ClassVar[str] = 'prefix_pk'


class BindingView(ConnectorView):
    """
    Class to retrieve information about bindings.
    """
    object_class = Binding
    source_name: ClassVar[str] = 'bindings'
    object_pk_name: ClassVar[str] = 'binding_pk'


client = ClientView.as_view()
global_type = GlobalTypeView.as_view()
global_element = GlobalElementView.as_view()
prefix = PrefixView.as_view()
binding = BindingView.as_view()
