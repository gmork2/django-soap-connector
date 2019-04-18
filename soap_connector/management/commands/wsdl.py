from django.core.management.base import BaseCommand, CommandError

from zeep.client import Transport
from zeep.wsdl import Document


class Command(BaseCommand):
    help = 'Print a WSDL Document'

    def add_arguments(self, parser):
        """

        :param parser:
        :return:
        """
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        """

        :param args:
        :param options:
        :return:
        """
        wsdl = options.get('url', None)
        transport = Transport()

        try:
            document = Document(wsdl, transport)
        except Exception as e:
            raise CommandError(e)

        document.dump()
