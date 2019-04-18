import operator

from django.core.management.base import BaseCommand, CommandError
from zeep.client import Client


class Command(BaseCommand):
    help = 'Print a WSDL Document'

    def add_arguments(self, parser):
        parser.add_argument('wsdl', type=str)

    def handle(self, *args, **options):
        wsdl = options['wsdl']
        if wsdl:
            client = Client(wsdl)
            self.stdout.write('')
            self.stdout.write("Prefixes:")
            for prefix, namespace in self.types.prefix_map.items():
                self.stdout.write(' ' * 4, '%s: %s' % (prefix, namespace))
    
            self.stdout.write('')
            self.stdout.write("Global elements:")
            for elm_obj in sorted(client.wsdl.types.elements, key=lambda k: k.qname):
                value = elm_obj.signature(schema=client.wsdl.types)
                self.stdout.write(' ' * 4, value)
    
            self.stdout.write('')
            self.stdout.write("Global types:")
            for type_obj in sorted(client.wsdl.types.types, key=lambda k: k.qname or ''):
                value = type_obj.signature(schema=client.wsdl.types)
                self.stdout.write(' ' * 4, value)
    
            self.stdout.write('')
            self.stdout.write("Bindings:")
            for binding_obj in sorted(client.wsdl.bindings.values(), key=lambda k: str(k)):
                self.stdout.write(' ' * 4, str(binding_obj))
    
            print('')
            for service in client.wsdl.services.values():
                self.stdout.write(str(service))
                for port in service.ports.values():
                    self.stdout.write(' ' * 4, str(port))
                    self.stdout.write(' ' * 8, 'Operations:')
    
                    operations = sorted(
                        port.binding._operations.values(),
                        key=operator.attrgetter('name'))
    
                    for operation in operations:
                        self.stdout.write('%s%s' % (' ' * 12, str(operation)))
                    self.stdout.write('')