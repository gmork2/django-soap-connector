from typing import Type, List, ClassVar

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework.serializers import Serializer

from soap_connector.cache import Cache, Context

URL_NAMES = []


@api_view()
def root(request):
    """

    :param request:
    :return:
    """
    return Response({
        f'{name}': reverse(f'soap_connector:{name}_list', request=request)
        for name in URL_NAMES
    })


class SerializerMixin(object):
    """

    """
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


class BaseAPIView(SerializerMixin, APIView):
    """

    """
    object_class: ClassVar[type] = None

    @property
    def cache(self) -> Cache:
        """

        :return:
        """
        context: Context = self.get_serializer_context()
        cache = Cache(context)

        return cache

    def list(self, request: Request, **kwargs) -> Response:
        """

        :param request:
        :return:
        """
        object_list: List[dict] = self.cache.values()
        if object_list:
            return Response(object_list, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, **kwargs) -> Response:
        """

        :param request:
        :return:
        """
        pk: int = kwargs.get('pk', None)
        if pk is None:
            return self.list(request)
        else:
            data: dict = self.cache[pk]
            if data is not None:
                return Response(data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request: Request, **kwargs) -> Response:
        """

        :param request:
        :return:
        """
        pass

    def delete(self, request: Request, **kwargs) -> Response:
        """

        :param request:
        :return:
        """
        pass

    def put(self, request: Request, **kwargs) -> Response:
        """

        :param request:
        :return:
        """
        pass
