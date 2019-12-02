from setuptools import setup, find_packages

setup(
    name='django-soap-connector',
    version='1.0.0',
    packages=['api', 'tests', 'tests.api', 'tests.cache', 'tests.client', 'management', 'management.commands',
              'serializers'],
    package_dir={'': 'soap_connector'},
    url='https://github.com/gmork2/django-soap-connector',
    license='GNU General Public License v3.0',
    author='fernando',
    author_email='gmork.02@gmail.com',
    description='Django app to connect to an existing SOAP web service and transform it into a REST API.',

    install_requires=['django', 'djangorestframework', 'zeep'],
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': [],
    },
)
