import sys
import os

from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponseRedirect
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


settings.configure(
    DEBUG=True,
    SECRET_KEY='A-random-secret-key!',
    ROOT_URLCONF=sys.modules[__name__],
    ALLOWED_HOST=['127.0.0.1', 'localhost'],
    STATIC_URL='/static/',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'rest_framework',
        'soap_connector'
    ),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        },
    ],
    REST_FRAMEWORK={
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.AllowAny',
        )
    })

urlpatterns = [
    url(r'^$', lambda r: HttpResponseRedirect('api/')),
    url(r'^api/', include(('soap_connector.urls', 'soap_connector'), namespace='soap_connector')),
]
urlpatterns += static('static', view=serve)

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
