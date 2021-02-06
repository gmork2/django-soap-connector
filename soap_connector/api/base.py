from typing import Type, List, ClassVar, Optional
from contextlib import contextmanager

from django.core.cache import cache

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

URL_NAMES = [
    'settings', 'client', 'signature', 'username_token', 'registry'
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
        f'{name}': reverse(f'soap_connector:{name}_list', request=request)
        for name in URL_NAMES
    })


@api_view()
def registry(request):
    """

    :param request:
    :return:
    """
    response = dict()
    versions = {k: cache.get(k) for k in Registry.store}

    for key, value in versions.items():
        user_id = key.split(':')[0]
        response[key] = {}
        for cls, pk_list in value.items():
            response[key][cls] = {}
            for pk in pk_list:
                data = cache.get(':'.join([user_id, cls]), version=pk)
                response[key][cls][pk] = data
    return Response(response)


class SerializerMixin(object):
    """
    Mixin that provides a serializer class that should be used
    for validating and deserializing input, and for serializing
    output.
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


# TODO: Default allowed methods
class BaseAPIView(SerializerMixin, APIView):
    """
    This class extends REST framework's APIView class, adding
    commonly required behavior for standard list and detail views.
    """
    object_class: ClassVar[type] = None
    object_pk_name: ClassVar[str] = None
    lookup_url_kwarg = 'client_pk'

    get_context = SerializerMixin.get_serializer_context

    def set_context(self, object_class: type,
                    serializer_class: Type[Serializer] = None) -> None:
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
    def with_context(self, object_class: type,
                     serializer_class: Type[Serializer] = None) -> None:
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
        obj = self.cache[pk]
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
        if self.object_pk_name in kwargs:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        obj = self.get_object(pk)
        if obj:
            del obj
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Concrete view for updating an object.

        :param request:
        :return:
        """
        if self.object_pk_name not in kwargs or \
                kwargs[self.object_pk_name] not in self.cache:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            context: Context = self.get_serializer_context()
            serializer = self.serializer_class(
                data=request.data, context=context
            )
            if serializer.is_valid():
                data = serializer.update(None, serializer.data)
                return Response(data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


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
        with self.with_context(Client):
            try:
                connector = Connector.from_view(self)
            except (CacheError, ConnectorError):
                return Response(status=status.HTTP_409_CONFLICT)
            else:
                data = getattr(connector, self.source_name, None)
                if data:
                    self.save(data)
                    return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def save_all(self, object_list, cls, lookup=None):
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
                    self.save_all(item[key], cls, lookup)

            except StopIteration:
                break

    def save(self, object_list):
        """
        Saves an object list.

        :param object_list:
        :return:
        """
        self.save_all(object_list, Client)
