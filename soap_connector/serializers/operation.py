from typing import List, Optional

from rest_framework import serializers

from zeep.wsdl.messages.soap import SoapMessage


def parser(parts: Optional[List[str]] = ()):
    """
    Returns a parser signature.

    :param parts:
    :return:
    """
    for part in parts:
        params = part.split(', ')
        for param in params:
            qname, _type = param.split(': ')
            yield qname, _type


def signature(soap_message: SoapMessage):
    """

    :param soap_message:
    :return:
    """
    parts = []

    return parts


class OperationSerializer(serializers.Serializer):
    """

    """
    pass
