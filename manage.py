import sys

from django.conf import settings
from django.core.management import execute_from_command_line

settings.configure(
    DEBUG=True,
    SECRET_KEY='A-random-secret-key!',
    ROOT_URLCONF=sys.modules[__name__],
    INSTALLED_APPS = (
        'django.contrib.admin',
        'soap_connector'
    ),
)

if __name__ == '__main__':
    execute_from_command_line(sys.argv)