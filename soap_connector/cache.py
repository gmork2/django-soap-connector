import logging
from typing import Dict, List, Union, Optional

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

    def __str__(self):
        """

        :return:
        """
        return f'{self.key} -> {cache.get(self.key, None)}'


class Cache(object):
    """
    Cache protocol wrapping django's cache.
    """
    def __init__(self, context: Context):
        """

        :param context:
        """
        self.key: Optional[str] = None
        self.registry: Optional[Registry] = None
        self.timeout = None

        self.set_context(context)

    def __getitem__(self, version: int) -> dict:
        """

        :param version:
        :return:
        """
        data: dict = cache.get(self.key, version=version)
        return data

    def __setitem__(self, version: int, data: dict) -> None:
        """

        :param version:
        :param data:
        :return:
        """
        cache.set(self.key, data, timeout=self.timeout, version=version)
        self.registry.insert(version)

    def __delitem__(self, version) -> None:
        """


        :param version:
        :return:
        """
        if self[version]:
            cache.delete(self.key, version=version)
            self.registry.remove(version)

    def __contains__(self, version: int):
        """

        :param version:
        :return:
        """
        versions = self.registry.retrieve()
        return version in versions

    def set_context(self, context: Context) -> None:
        """

        :param context:
        :return:
        """
        cls: type = context['view'].object_class

        self.key: str = make_key(context, cls.__name__)
        self.registry = Registry(context)

    def values(self) -> ObjectList:
        """

        :return:
        """
        return [
            cache.get(self.key, version=version)
            for version in self.registry.retrieve()
        ]
