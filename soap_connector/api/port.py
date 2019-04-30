from typing import ClassVar

from zeep.wsdl.definitions import Port

from soap_connector.api.client import ConnectorView


class PortView(ConnectorView):
    object_class = Port
    source_name: ClassVar[str] = 'ports'
    object_pk_name: ClassVar[str] = 'port_pk'


port = PortView.as_view()
