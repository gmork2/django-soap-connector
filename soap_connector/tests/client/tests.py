from django.contrib.auth.models import AnonymousUser
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase


class ClientViewTestCase(APITestCase):
    """

    """
    def setUp(self):
        """

        :return:
        """
        self.url = reverse("soap_connector:client_list")

        self.request = APIRequestFactory().get(self.url)
        self.request.user = AnonymousUser()

    def test_simple(self):
        """

        :return:
        """
        url = reverse("soap_connector:root")
        response = self.client.get(url)

        self.assertIn(
            self.request.build_absolute_uri(),
            response.data.values()
        )

    def test_get_empty_client_list(self):
        """

        :return:
        """
        response = self.client.get(self.url)

        self.assertEqual(404, response.status_code)
        self.assertFalse(response.data)

    def tearDown(self):
        """

        :return:
        """
        pass
