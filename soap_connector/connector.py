import logging

from zeep.client import Client

logger = logging.getLogger(__name__)


class Connector(object):
    """

    """
    def __init__(self, client: dict, **kwargs):
        """

        :param kwargs:
        """
        self.client = Client(**client)
