from typing import ClassVar

from zeep.wsdl.definitions import Service, Port, Operation

from soap_connector.api.client import ConnectorView


class ServiceView(ConnectorView):
    """

    """
    object_class = Service
    source_name: ClassVar[str] = 'services'
    object_pk_name: ClassVar[str] = 'service_pk'

    def save(self, object_list):
        """
        Saves service, ports and operations objects.

        :param object_list:
        :return:
        """
        lookup = [
            ('ports', Port),
            ('operations', Operation)
        ]
        self.save_all(object_list, Service, lookup)


service = ServiceView.as_view()
