from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

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
