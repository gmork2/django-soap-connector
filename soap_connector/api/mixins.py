from typing import Type, ClassVar

from rest_framework.request import Request
from rest_framework.serializers import Serializer

from soap_connector.cache import Cache, Context


class SerializerMixin(object):
    """
    Mixin that provides a serializer class that should be used
    for validating and deserializing input, and for serializing
    output.
    """
    request: Request = None
    serializer_class: ClassVar[Type[Serializer]] = None

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for
        validating and deserializing input, and for serializing
        output.
        """
        serializer_class: Type[Serializer] = \
            self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()

        return serializer_class(*args, **kwargs)

    def get_serializer_class(self) -> Type[Serializer]:
        """
        Provide different serializations depending on the
        object class.

        :return:
        """
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__)

        return self.serializer_class

    def get_serializer_context(self) -> Context:
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self
        }
