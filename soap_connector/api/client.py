import logging
from typing import ClassVar

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from zeep.client import Client

from soap_connector.serializers import ClientSerializer
from soap_connector.api.base import BaseAPIView
from soap_connector.connector import Connector

logger = logging.getLogger(__name__)


class ClientView(BaseAPIView):
    """

    """
    serializer_class = ClientSerializer
    object_class = Client


class ConnectorView(ClientView):
    """

    """
    source_name: ClassVar[str] = ''
    object_pk_name: ClassVar[str] = ''

    @property
    def allowed_methods(self):
        """

        :return:
        """
        return ['GET']

    def list(self, request: Request, **kwargs) -> Response:
        """

        :param request:
        :param kwargs:
        :return:
        """
        object_class = self.object_class

        self.set_context(Client)
        connector = Connector.from_view(self)
        data = getattr(connector, self.source_name)

        if data:
            self.set_context(object_class)
            self.save(data)
            return Response(data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, **kwargs) -> Response:
        """

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

    def save(self, object_list):
        """

        :param object_list:
        :return:
        """
        for obj in object_list:
            self.cache[obj['pk']] = obj


client = ClientView.as_view()
