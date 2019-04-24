import logging

from zeep.wsse import Signature

from soap_connector.serializers import SignatureSerializer, UsernameTokenSerializer
from soap_connector.api.base import BaseAPIView

logger = logging.getLogger(__name__)


class SignatureView(BaseAPIView):
    """

    """
    serializer_class = SignatureSerializer
    object_class = Signature
