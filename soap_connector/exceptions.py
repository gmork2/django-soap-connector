from typing import Any


class ConnectorError(Exception):
    """
    Basic exception for errors raised by connector.
    """
    def __init__(self, instance: Any, msg: str = None):
        if msg is None:
            msg = f"An error occurred with connector {instance}"
        super().__init__(msg)
        self.instance = instance
