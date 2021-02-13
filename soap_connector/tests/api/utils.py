from soap_connector.api.base import BaseAPIView
from soap_connector.serializers.base import BaseSerializer

_counter = 0


def set_name():
    """
    Return a new dummy name each time this function
    is invoked.

    :return:
    """
    global _counter

    _counter += 1
    return 'Dummy' + str(_counter)


class DummySerializer(BaseSerializer):
    """

    """
    pass


class DummyView(BaseAPIView):
    """
    This view allows generating instances with unique
    context.
    """
    serializer_class = DummySerializer
    lookup_url_kwarg = 'pk'

    def __new__(cls, *args, **kwargs):
        """
        Set a different object_class for each instance.

        :param args:
        :param kwargs:
        :return:
        """
        new_cls = super().__new__(cls)

        new_cls.object_class = type(
            set_name(), (object, ), {}
        )
        return new_cls
