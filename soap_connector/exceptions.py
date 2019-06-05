from typing import Type, Any


class ConnectorError(Exception):
    """
    Basic exception for errors raised by connector.
    """
    def __init__(self, instance: Any, msg: str = None):
        if msg is None:
            msg = f"An error occurred with connector {instance}"
        super().__init__(msg)
        self.instance = instance


class CacheError(Exception):
    """
    Exception for cache access error.
    """
    def __init__(self, instance: Type, cache: "Cache", pk: int):
        super().__init__(
            instance,
            f"{instance}: I can't retrieve item for {cache.registry.cls} with pk={pk}"
        )
        self.cache = cache
        self.pk = pk
