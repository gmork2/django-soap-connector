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
        pass

    def get(self, request: Request, **kwargs) -> Response:
        """

        :param request:
        :param kwargs:
        :return:
        """
        pass

    def save(self, object_list):
        """

        :param object_list:
        :return:
        """
        pass


client = ClientView.as_view()
