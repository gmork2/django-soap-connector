import logging
from typing import Dict, List, Any, Union, Optional

from django.core.cache import cache

logger = logging.getLogger(__name__)

ObjectList = List[Optional[dict]]
Context = Dict[
    str,
    Union[
        "api.base.BaseAPIView",
        "rest_framework.request.Request"
    ]
]


def make_key(context, sufix: str) -> str:
    """

    :return:
    """
    return ':'.join([
        str(context['request'].user.id),
        sufix
    ])


class Cache(object):
    """
    Cache protocol wrapping django's cache.
    """
    def __init__(self, context: Context):
        """

        :param context:
        """
        self.key: Optional[str] = None
        self.context = context

    def __getitem__(self, item):
        """

        :param item:
        :return:
        """
        return cache[item]

    def __setitem__(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        cache[key] = value

    def __delitem__(self, key):
        """

        :param key:
        :return:
        """
        del cache[key]
