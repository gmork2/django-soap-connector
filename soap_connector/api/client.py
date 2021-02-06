import logging
from typing import ClassVar

from zeep.client import Client
from zeep.wsdl.definitions import Binding
from zeep.xsd.types import Type
from zeep.xsd.elements import Element

from soap_connector.serializers import ClientSerializer
from soap_connector.api.base import BaseAPIView, ConnectorView


logger = logging.getLogger(__name__)


class ClientView(BaseAPIView):
    """
    This class defines a CRUD interface for client objects.
    """
    serializer_class = ClientSerializer
    object_class = Client
    object_pk_name: ClassVar[str] = 'client_pk'


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
