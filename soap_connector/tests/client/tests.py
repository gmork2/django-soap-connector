from copy import copy

from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase


def request_factory(url):
    """

    :param url:
    :return:
    """
    request = APIRequestFactory().get(url)
    request.user = AnonymousUser()

    return request


class ClientViewTestCase(APITestCase):
    """

    """
    def setUp(self):
        """

        :return:
        """
        self.url = reverse("soap_connector:client_list")
        self.data = {
            'wsdl': 'https://graphical.weather.gov/xml/DWMLgen/wsdl/ndfd'
        }

    def test_simple(self):
        """

        :return:
        """
        url = reverse("soap_connector:root")

        response = self.client.get(url)
        request = request_factory(self.url)

        self.assertIn(
            request.build_absolute_uri(),
            response.data.values()
        )

    def test_get_list(self):
        """

        :return:
        """

    def test_get_empty_list(self):
        """

        :return:
        """
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.data)

    def test_post(self):
        """

        :return:
        """
        response = self.client.post(self.url, self.data)
        data = response.data
        self.assertNotContains(response, 'non_field_errors', status_code=200)

        response = self.client.get(data['url'])
        self.assertEqual(data, response.data)

    def test_update_post(self):
        """

        :return:
        """
        data = copy(self.data)
        data['pk'] = '2'
        response = self.client.post(self.url, data)

        self.assertTrue(response.data['pk'] == 1)

        url = reverse(
            "soap_connector:client_detail",
            kwargs={'pk': '1'}
        )
        response = self.client.post(url, self.data)
        self.assertContains(response, '', status_code=400)

    def test_get(self):
        """

        :return:
        """
        response = self.client.post(self.url, self.data)
        url = reverse(
            "soap_connector:client_detail",
            kwargs={'pk': response.data['pk']})
        r = self.client.get(url)

        self.assertDictEqual(r.data, response.data)

    def test_get_non_existent(self):
        """

        :return:
        """
        url = reverse(
            "soap_connector:client_detail",
            kwargs={'pk': '1'})
        response = self.client.get(url)

        self.assertContains(response, '', status_code=404)

    def test_delete(self):
        """

        :return:
        """
        response = self.client.post(self.url, self.data)
        url = reverse(
            "soap_connector:client_detail",
            kwargs={'pk': response.data['pk']})
        r = self.client.delete(url)

        self.assertContains(r, '', status_code=204)
        self.assertIsNone(r.data)

    def test_delete_non_existent(self):
        """

        :return:
        """
        url = reverse(
            "soap_connector:client_detail",
            kwargs={'pk': '1'})
        response = self.client.delete(url)

        self.assertContains(response, '', status_code=404)

    def test_put(self):
        """

        :return:
        """
        data = {
            'wsdl': 'http://www.dataaccess.com/webservicesserver/numberconversion.wso?WSDL'
        }
        response = self.client.post(self.url, self.data)
        url = reverse(
            "soap_connector:client_detail",
            kwargs={'pk': response.data['pk']})
        r = self.client.put(url, data)

        self.assertNotEqual(r.data, response.data)

    def test_update_non_existent(self):
        """

        :return:
        """
        url = reverse(
            "soap_connector:client_detail",
            kwargs={'pk': 1})
        r = self.client.put(url, self.data)

        self.assertContains(r, '', status_code=400)

    def test_create_put(self):
        """

        :return:
        """
        response = self.client.put(self.url, self.data)
        self.assertContains(response, '', status_code=400)

    def tearDown(self):
        """

        :return:
        """
        cache.clear()
