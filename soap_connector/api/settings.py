import logging

from zeep.settings import Settings

from soap_connector.serializers import SettingsSerializer
from soap_connector.api.base import BaseAPIView

logger = logging.getLogger(__name__)


class SettingsView(BaseAPIView):
    """

    """
    serializer_class = SettingsSerializer
    object_class = Settings


settings = SettingsView.as_view()
