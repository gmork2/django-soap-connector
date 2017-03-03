from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Print a WSDL Document'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass