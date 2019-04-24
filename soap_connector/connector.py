import logging

from zeep.client import Client

logger = logging.getLogger(__name__)


def to_number(s: str) -> int:
    """
    Transform 's' parameter into number and returns it.

    :param s:
    :return:
    """
    return int.from_bytes(s.encode(), 'little')


class Connector(object):
    """

    """
    def __init__(self, client: dict, **kwargs):
        """

        :param kwargs:
        """
        self.client = Client(**client)
