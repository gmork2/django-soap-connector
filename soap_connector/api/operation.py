from typing import ClassVar

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer

from zeep.wsdl.definitions import Operation

from soap_connector.api.client import ConnectorView
from soap_connector.serializers import OperationSerializer
from soap_connector.cache import Context


class OperationView(ConnectorView):
    object_class = Operation
    serializer_class = OperationSerializer
    source_name: ClassVar[str] = 'operations'
    object_pk_name: ClassVar[str] = 'operation_pk'

    @property
    def allowed_methods(self):
        """

        :return:
        """
        return ['GET', 'POST']

    def post(self, request: Request, **kwargs) -> Response:
        """

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


operation = OperationView.as_view()
