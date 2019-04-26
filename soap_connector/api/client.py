import logging

from zeep.client import Client

from soap_connector.serializers import ClientSerializer
from soap_connector.api.base import BaseAPIView

logger = logging.getLogger(__name__)


class ClientView(BaseAPIView):
    """

    """
    serializer_class = ClientSerializer
    object_class = Client


client = ClientView.as_view()
