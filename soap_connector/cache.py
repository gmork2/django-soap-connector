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


class Registry(object):
    """

    """
    def __init__(self, context):
        """

        :return:
        """
        self.key: str = make_key(context, 'versions')
        self.cls: type = context['view'].object_class

        data = self.retrieve()

        if isinstance(data, dict):
            cache.set(self.key, data)

    def retrieve(self) -> Union[Dict[str, list], List[int]]:
        """

        :return:
        """

        registry: dict = cache.get(self.key)

        if registry:
            return registry.get(self.cls.__name__, [])
        return {self.cls.__name__: []}

    def insert(self, version: int) -> None:
        """

        :param version:
        :return:
        """
        versions: List[int] = self.retrieve()

        if version not in versions:
            versions.append(version)
            self.update(versions)

    def remove(self, version: int) -> None:
        """

        :param version:
        :return:
        """
        versions: List[int] = self.retrieve()

        if version in versions:
            versions.remove(version)
            self.update(versions)

    def update(self, versions: List[int]) -> None:
        """

        :param versions:
        :return:
        """
        data = {
            **cache.get(self.key),
            **{self.cls.__name__: versions}
        }
        cache.set(self.key, data)


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
