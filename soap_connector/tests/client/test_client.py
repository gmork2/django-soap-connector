from copy import copy
from unittest import skip

import requests

from django.contrib.auth.models import AnonymousUser

from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from cache import Registry


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
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.wsdl = 'https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
        response = requests.get(cls.wsdl)
        cls.failed = True if response.status_code != 200 else False

    def setUp(self):
        """

        :return:
        """
        if self.failed:
            self.skipTest("Test skipped because service is not available!")

        Registry.sessions = set()

        self.url = reverse("soap_connector:client_list")
        self.data = {
            'wsdl': self.wsdl
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

    @skip
    def test_get_list(self):
        """

        :return:
        """

    def test_get_empty_list(self):
        """

        :return:
        """
        url = reverse(
            "soap_connector:client_detail",
            kwargs={'client_pk': '1'}
        )
        self.client.delete(url)
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

        self.assertTrue(int(response.data['pk']) == int(data['pk']))

        url = reverse(
            "soap_connector:client_detail",
            kwargs={'client_pk': '1'}
        )
        response = self.client.post(url, self.data)
        self.assertContains(response, '', status_code=405)

    def test_get(self):
        """

        :return:
        """
        response = self.client.post(self.url, self.data)
        url = reverse(
            "soap_connector:client_detail",
            kwargs={'client_pk': response.data['pk']})
        r = self.client.get(url)

        self.assertDictEqual(r.data, response.data)

    def test_get_non_existent(self):
        """

        :return:
        """
        url = reverse(
            "soap_connector:client_detail",
            kwargs={'client_pk': '2'})
        response = self.client.get(url)

        self.assertContains(response, '', status_code=404)

    def test_delete(self):
        """

        :return:
        """
        response = self.client.post(self.url, self.data)
        url = reverse(
            "soap_connector:client_detail",
            kwargs={'client_pk': response.data['pk']})
        r = self.client.delete(url)

        self.assertContains(r, '', status_code=204)
        self.assertIsNone(r.data)

    def test_delete_non_existent(self):
        """

        :return:
        """
        url = reverse(
            "soap_connector:client_detail",
            kwargs={'client_pk': '1'})
        response = self.client.delete(url)

        self.assertContains(response, '', status_code=404)

    def test_update_non_existent(self):
        """

        :return:
        """
        url = reverse(
            "soap_connector:client_detail",
            kwargs={'client_pk': 1})
        r = self.client.put(url, self.data)

        self.assertContains(r, '', status_code=405)

    def test_create_put(self):
        """

        :return:
        """
        response = self.client.put(self.url, self.data)
        self.assertContains(response, '', status_code=405)

