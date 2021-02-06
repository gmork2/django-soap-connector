import logging
from typing import Dict, List, Union, Optional, Type

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


def make_key(context: Context, sufix: str) -> str:
    """
    A custom key function for processing to the final key.

    :return:
    """
    return ':'.join([
        str(context['request'].user.id) or str(0),
        sufix
    ])


class SingletonDecorator:
    """

    """
    def __init__(self, cls: Type):
        """

        :param cls:
        """
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        """

        :param args:
        :param kwds:
        :return:
        """
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)

        return self.instance


class CacheIterator(object):
    """
    Caches the elements in iterable object according context
    provided by view.
    """
    pk_name = 'pk'

    def __init__(self, object_list: ObjectList, cls: type,
                 view: "BaseAPIView"):
        """
        Initialize the iterator.

        :param object_list:
        :param cls:
        :param view:
        """
        self.index = 0

        self.object_list = object_list
        self.cls = cls
        self.view = view

    def __iter__(self) -> "CacheIterator":
        """
        Returns the iterator object.

        :return:
        """
        return self

    def __next__(self) -> dict:
        """
        Caches and returns the object of the current iteration.

        :return:
        """
        try:
            obj = self.object_list[self.index]
        except IndexError:
            raise StopIteration

        self.index += 1

        with self.view.with_context(self.cls):
            self.view.cache[obj[self.pk_name]] = obj
            return obj


class Registry(object):
    """
    Manages a registry of cache versions for each context.
    """
    store = list()

    def __init__(self, context: Context):
        """
        Initialize the registry using provided context.

        :return:
        """
        self.key: str = make_key(context, 'versions')
        self.cls: type = context['view'].object_class

        data = self.retrieve()

        if not data:
            self.reset()

    def retrieve(self) -> Union[Dict[str, list], List[int]]:
        """
        Retrieve a list of cache versions.

        :return:
        """
        registry: dict = cache.get(self.key)

        if registry:
            return registry.get(self.cls.__name__, [])
        return []

    def insert(self, version: int, timeout: float = None) -> None:
        """
        Adds a version in the registry.

        :param version:
        :param timeout:
        :return:
        """
        versions: List[int] = self.retrieve()

        if version not in versions:
            versions.append(version)
            self.update(versions, timeout)

    def remove(self, version: int) -> None:
        """
        Removes a version from the registry.

        :param version:
        :return:
        """
        versions: List[int] = self.retrieve()

        if version in versions:
            versions.remove(version)
            self.update(versions)

    def update(self, versions: List[int], timeout: float = None) -> None:
        """
        Updates the contents of the cache registry.

        :param versions:
        :param timeout:
        :return:
        """
        data = {
            **cache.get(self.key),
            **{self.cls.__name__: versions}
        }
        cache.set(self.key, data, timeout=timeout)
        self.store.append(self.key)

    def reset(self) -> None:
        """
        Reset registry in current context.

        :return:
        """
        data = {self.cls.__name__: []}
        cache.set(self.key, data)
        self.store.append(self.key)

    def __str__(self):
        """
        Displays the contents of the record for the current
        context.

        :return:
        """
        return f'{self.key} -> {cache.get(self.key, None)}'


class Cache(object):
    """
    Cache protocol wrapping django's cache.
    """
    def __init__(self, context: Context):
        """
        Initialize the cache object.

        :param context:
        """
        self.key: Optional[str] = None
        self.registry: Optional[Registry] = None
        self.timeout: Optional[float] = None

        self.set_context(context)

    def __getitem__(self, version: int) -> Optional[dict]:
        """
        Gets element from cache by version.

        :param version:
        :return:
        """
        if version in self:
            data: dict = cache.get(self.key, version=version)
            return data

    def __setitem__(self, version: int, data: dict) -> None:
        """
        Sets element to cache by version.

        :param version:
        :param data:
        :return:
        """
        cache.set(self.key, data, timeout=self.timeout, version=version)
        self.registry.insert(version, self.timeout)

    def __delitem__(self, version) -> None:
        """
        Removes element from cache by version.

        :param version:
        :return:
        """
        if self[version]:
            cache.delete(self.key, version=version)
            self.registry.remove(version)

    def __contains__(self, version: int):
        """
        Returns true if registry contains the version for the
        current context, otherwise returns false.

        :param version:
        :return:
        """
        versions = self.registry.retrieve()
        return version in versions

    def set_context(self, context: Context) -> None:
        """
        Initializes the registry with the provided context and
        generates a key used to save items in cache.

        :param context:
        :return:
        """
        cls: type = context['view'].object_class

        self.key: str = make_key(context, cls.__name__)
        self.registry = Registry(context)

    def values(self) -> ObjectList:
        """
        Returns a list of items from cache.

        :return:
        """
        return [
            cache.get(self.key, version=version)
            for version in self.registry.retrieve()
        ]

    @staticmethod
    def clear() -> None:
        """
        Delete all the keys in the cache, not just the keys set
        by this application.

        :return:
        """
        cache.clear()
