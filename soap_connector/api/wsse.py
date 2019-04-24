import logging

from zeep.wsse import Signature, UsernameToken

from soap_connector.serializers import SignatureSerializer, UsernameTokenSerializer
from soap_connector.api.base import BaseAPIView

logger = logging.getLogger(__name__)


class SignatureView(BaseAPIView):
    """

    """
    serializer_class = SignatureSerializer
    object_class = Signature


class UsernameTokenView(BaseAPIView):
    """

    """
    serializer_class = UsernameTokenSerializer
    object_class = UsernameToken


signature = SignatureView.as_view()
username_token = UsernameTokenView.as_view()
