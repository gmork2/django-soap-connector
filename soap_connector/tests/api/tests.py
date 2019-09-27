from unittest import skip
from copy import copy

from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from soap_connector.tests.api.utils import DummyView, BaseSerializer, set_name


class BaseTestCase(TestCase):
    """

    """
    def setUp(self):
        """

        :return:
        """
        url = reverse("soap_connector:root")

        request = APIRequestFactory().get(url)
        request.user = AnonymousUser()

        self.view = DummyView(request=request)
        self.context = {
            'request': request,
            'view': self.view
        }

    def test_get_serializer(self):
        """

        :return:
        """
        self.assertIsInstance(
            self.view.get_serializer(),
            self.view.get_serializer_class()
        )

    def test_get_serializer_class(self):
        """

        :return:
        """
        self.assertTrue(
            issubclass(
                self.view.get_serializer_class(),
                serializers.Serializer
            )
        )

    def get_serializer_context(self):
        """

        :return:
        """
        self.assertDictEqual(
            self.context,
            self.view.get_serializer_context()
        )

    @skip("For the moment used as alias")
    def test_get_context(self):
        """

        :return:
        """

    def test_non_serializer_class(self):
        """

        :return:
        """
        self.view.serializer_class = None

        self.assertRaises(
            AssertionError,
            self.view.get_serializer
        )

    def test_set_context(self):
        """

        :return:
        """
        view = copy(self.view)

        object_class = type(set_name(), (), {})
        serializer_class = BaseSerializer

        self.view.set_context(object_class, serializer_class)
        self.view.cache[1] = {'pk': 1}
        self.assertIsNone(view.cache[1])

    def test_context_manager(self):
        """

        :return:
        """
        view = copy(self.view)

        object_class = type(set_name(), (), {})
        serializer_class = BaseSerializer
        view.set_context(object_class, serializer_class)

        view.cache[1] = {'pk': 1}

        with self.view.with_context(object_class, serializer_class):
            self.assertDictEqual(
                view.cache[1], self.view.cache[1]
            )

        self.assertIsNone(self.view.cache[1])

    def test_cache(self):
        """

        :return:
        """
        self.assertTrue(hasattr(self.view, 'cache'))

        self.view.cache[1] = {'pk': 1}
        self.assertEqual(self.view.cache[1], {'pk': 1})

    def test_get_object(self):
        """

        :return:
        """
        data = {'pk': 1}
        self.view.cache[1] = data

        self.assertEqual(self.view.get_object(1), data)

    @skip("See client.tests")
    def test_list(self):
        """

        :return:
        """

    @skip("See client.tests")
    def test_get(self):
        """

        :return:
        """

    @skip("See client.tests")
    def test_post(self):
        """

        :return:
        """

    @skip("See client.tests")
    def test_delete(self):
        """

        :return:
        """

    @skip("See client.tests")
    def test_put(self):
        """

        :return:
        """

    def tearDown(self):
        """

        :return:
        """
        cache.clear()
