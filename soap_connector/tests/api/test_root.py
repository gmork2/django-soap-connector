from urllib.parse import urlparse, ParseResult

from django.test import TestCase
from django.urls import resolve, ResolverMatch
from rest_framework.reverse import reverse

from soap_connector.api.base import URL_NAMES


class RootTestCase(TestCase):
    """

    """
    def setUp(self):
        """

        :return:
        """
        self.url = reverse("soap_connector:root")
        self.response = self.client.get(self.url)

    def test_simple(self):
        """

        :return:
        """
        self.assertEqual(200, self.response.status_code)

    def test_url_names(self):
        """

        :return:
        """
        self.assertSetEqual(
            set(self.response.data.keys()),
            set(URL_NAMES)
        )

    def test_endpoints(self):
        """
        Endpoint url path must correspond to a view
        function .

        :return:
        """
        for url in self.response.data.values():
            link = ParseResult('', '', *urlparse(url)[2:]).geturl()
            self.assertIsInstance(resolve(link), ResolverMatch)

