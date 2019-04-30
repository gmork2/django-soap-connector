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

        :param object_list:
        :return:
        """
        for _service in object_list:
            self.set_context(Service)
            self.cache[_service['pk']] = _service

            for _port in _service['ports']:
                self.set_context(Port)
                self.cache[_port['pk']] = _port

                for _operation in _port['operations']:
                    self.set_context(Operation)
                    self.cache[_operation['pk']] = _operation
        self.set_context(Service)


service = ServiceView.as_view()
