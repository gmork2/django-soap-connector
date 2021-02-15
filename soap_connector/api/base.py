from typing import Type, List, ClassVar, Optional
from contextlib import contextmanager

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework.serializers import Serializer

from zeep.client import Client

from soap_connector.cache import Cache, Context
from soap_connector.cache import Registry
from soap_connector.connector import Connector
from soap_connector.cache import CacheIterator
from soap_connector.exceptions import ConnectorError, CacheError
from soap_connector.api.mixins import SerializerMixin

DEFAULT_DEPTH = 2
URL_NAMES = [
    'settings_list', 'client_list', 'signature_list', 'username_token_list', 'registry_list'
]


@api_view()
def root(request):
    """
    The API entry point that provide a list of top-level
    collections.

    :param request:
    :return:
    """
    return Response({
        f'{name}': reverse(f'soap_connector:{name}', request=request)
        for name in URL_NAMES
    })


@api_view()
def registry(request):
    """

    :param request:
    :return:
    """
    try:
        depth = int(request.query_params.get('depth', DEFAULT_DEPTH))
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(Registry.dump(depth=depth))


class BaseAPIView(SerializerMixin, APIView):
    """
    This class extends REST framework's APIView class, adding
    commonly required behavior for standard list and detail views.
    """
    object_class: ClassVar[type] = None
    object_pk_name: ClassVar[str] = None
    lookup_url_kwarg = 'client_pk'

    get_context = SerializerMixin.get_serializer_context

    def set_context(
            self,
            object_class: type,
            serializer_class: Type[Serializer] = None
    ) -> None:
        """
        Set a new context.

        :param object_class:
        :param serializer_class:
        :return:
        """
        self.object_class = object_class

        if serializer_class is not None:
            self.serializer_class = serializer_class

    @contextmanager
    def with_context(
            self,
            object_class: type,
            serializer_class: Type[Serializer] = None
    ) -> None:
        """
        Context manager that allows the executing of code in a
        different context.

        :param object_class:
        :param serializer_class:
        :return:
        """
        ctx = (
            self.object_class,
            self.serializer_class
        )
        self.set_context(object_class, serializer_class)
        yield self
        self.set_context(*ctx)

    @property
    def cache(self) -> Cache:
        """
        Property that returns a contextualized cache object.

        :return:
        """
        context: Context = self.get_context()
        cache = Cache(context)

        return cache

    def get_object(self, pk: Optional[int] = None) -> dict:
        """

        :param pk:
        :return:
        """
        _pk = pk or self.kwargs[self.lookup_url_kwarg]
        obj = self.cache[_pk]
        return obj

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Concrete view for listing a collection of objects.

        :param request:
        :return:
        """
        object_list: List[dict] = self.cache.values()
        return Response(object_list, status=status.HTTP_200_OK)

    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Concrete view for retrieve an object.

        :param request:
        :return:
        """
        pk: int = kwargs.get(self.object_pk_name, None)
        if pk is None:
            return self.list(request)

        data: Optional[dict] = self.get_object(pk)
        code: int = status.HTTP_200_OK if data else status.HTTP_404_NOT_FOUND

        return Response(data, status=code)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Concrete view for creating an object.

        :param request:
        :return:
        """
        context: Context = self.get_serializer_context()
        serializer: Serializer = self.serializer_class(
            data=request.data, context=context
        )
        if serializer.is_valid():
            data: dict = serializer.create(serializer.data)
            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Concrete view for deleting an object.

        :param request:
        :return:
        """
        pk: int = kwargs.get(self.object_pk_name, None)

        if pk in self.cache:
            del self.cache[pk]
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)


class ConnectorView(BaseAPIView):
    """
    Class to provide read-only methods to interact with a SOAP
    server through connector.
    """
    source_name: ClassVar[str] = ''

    @property
    def allowed_methods(self):
        """
        The list of HTTP method names that this view will
        accept.

        :return:
        """
        return ['GET']

    def list(self, request: Request, **kwargs) -> Response:
        """
        Concrete view for listing a collection of objects
        from connector.

        :param request:
        :param kwargs:
        :return:
        """
        try:
            with self.with_context(Client):
                connector = Connector.from_view(self)
        except (CacheError, ConnectorError):
            return Response(status=status.HTTP_409_CONFLICT)
        else:
            data = getattr(connector, self.source_name, None)
            if data:
                self.perform_create(data)
                return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def save(self, object_list, cls, lookup=None):
        """
        Iterates on object_list and its recursively nested lists.

        :param object_list: Current object list
        :param cls: Class to which the context belongs
        :param lookup: Indicates the sublists on which to nest
        :return:
        """
        iterator = CacheIterator(object_list, cls, self)

        while True:
            try:
                item = next(iterator)
                if lookup:
                    key, cls = lookup.pop(0)
                    self.save(item[key], cls, lookup)

            except StopIteration:
                break

    def perform_create(self, object_list):
        """
        Saves an object list.

        :param object_list:
        :return:
        """
        self.save(object_list, self.object_class)
