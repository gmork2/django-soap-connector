from unittest import skip
import time

from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from ..api.base import BaseAPIView
from ..serializers.base import BaseSerializer as Serializer
from ..cache import *

_counter = 0


def set_name():
    """
    Return a new dummy name each time this function
    is invoked.

    :return:
    """
    global _counter

    _counter += 1
    return 'Dummy' + str(_counter)


class DummyView(BaseAPIView):
    """
    This view allows generating instances with unique
    context.
    """
    serializer_class = Serializer

    def __new__(cls, *args, **kwargs):
        """
        Set a different object_class for each instance.

        :param args:
        :param kwargs:
        :return:
        """
        new_cls = super().__new__(cls)

        new_cls.object_class = type(
            set_name(), (object, ), {}
        )
        return new_cls


class BaseTestCase(TestCase):
    """
    Cache's base class.
    """
    def setUp(self):
        """

        :return:
        """
        url = reverse("soap_connector:root")

        request = APIRequestFactory().get(url)
        request.user = AnonymousUser()

        self.context = {
            'request': request,
            'view': DummyView(request=request)
        }

    def tearDown(self):
        """
        Delete all the keys in the cache.

        :return:
        """
        cache.clear()


class RegistryTestCase(BaseTestCase):
    """

    """
    def setUp(self):
        """

        :return:
        """
        super().setUp()

        self.registry = Registry(context=self.context)

    def test_simple(self):
        """

        :return:
        """
        pass


class CacheTestCase(BaseTestCase):
    """

    """
    def setUp(self):
        """

        :return:
        """
        super().setUp()

        self.cache = Cache(context=self.context)
        self.data = {
            'id': 1,
            'field': 'test_1'
        }

    def test_simple(self):
        """

        :return:
        """
        self.assertTrue(
            hasattr(self.context['view'], 'cache')
        )

    def test_set(self):
        """

        :return:
        """
        self.cache[1] = self.data
        self.cache[2] = data = {
            'id': 2,
            'field': 'test_2'
        }
        self.assertNotEqual(self.cache[1], data)
        self.assertEqual(self.cache[1], self.data)
        self.assertNotEqual(self.cache[2], self.data)
        self.assertEqual(self.cache[2], data)

    def test_get_empty_cache(self):
        """

        :return:
        """
        self.assertIsNone(self.cache[1])

    def test_delete(self):
        """

        :return:
        """
        self.cache[1] = self.data
        del self.cache[1]
        self.cache[2] = data = {
            'id': 2,
            'field': 'test_2'
        }

        self.assertIsNone(self.cache[1])
        self.assertEqual(self.cache[2], data)

    def test_delete_empty_cache(self):
        """
        Deletion in empty cache has no any effect.

        :return:
        """
        del self.cache[1]
        self.assertIsNone(self.cache[1])

    def test_float_timeout(self):
        """
        Make sure a timeout given as a float works.

        :return:
        """
        self.cache.timeout = 999999.9
        self.cache[1] = self.data

        self.assertEqual(self.cache[1], self.data)

    def test_in(self):
        """
        The in operator can be used to inspect cache
        contents.

        :return:
        """
        self.cache[1] = self.data

        self.assertIn(1, self.cache)
        self.assertNotIn(2, self.cache)

    @skip("Not implemented")
    def test_data_types(self):
        """
        Many different data types can be cached.

        :return:
        """

    def test_expiration(self):
        """
        Cache values can be set to expire.

        :return:
        """
        self.cache.timeout = 1
        self.cache[1] = self.data
        self.assertEqual(self.cache[1], self.data)

        time.sleep(2)
        self.assertIsNone(self.cache[1], self.data)

    def test_forever_timeout(self):
        """
        Passing in None into timeout results in a value
        that is cached forever.

        :return:
        """
        self.cache.timeout = 1
        self.cache[1] = self.data
        self.cache.timeout = None
        self.cache[2] = data2 = {
            'id': 2,
            'field': 'test_2'
        }
        time.sleep(2)
        self.assertIsNone(self.cache[1], self.data)
        self.assertEqual(self.cache[2], data2)

    def test_zero_timeout(self):
        """
        Passing in zero into timeout results in a value
        that is not cached.
        """
        self.cache.timeout = 0
        self.cache[1] = self.data

        self.assertIsNone(self.cache[1], self.data)

    def test_non_existent(self):
        """
        Nonexistent cache keys return as None/default.

        :return:
        """
        self.cache[1] = self.data
        self.assertIsNone(self.cache[2])

    def test_version(self):
        """
        Test for same cache key conflicts between versions.

        :return:
        """
        self.cache[1] = self.data
        self.cache[2] = data2 = {
            'id': 2,
            'field': 'test_2'
        }
        self.assertNotEqual(self.cache[1], data2)

    def test_clear(self):
        """
        The cache can be emptied using clear.

        :return:
        """
        self.cache[1] = self.data
        self.cache[2] = {
            'id': 2,
            'field': 'test_2'
        }
        self.cache.clear()

        self.assertIsNone(self.cache[1])
        self.assertIsNone(self.cache[2])

    def test_unicode(self):
        """
        Unicode values can be cached.

        :return:
        """
        data = {
            'ascii': 'ascii_value',
            'unicode_ascii': 'Iñtërnâtiônàlizætiøn',
            'ascii2': {'x': 1}
        }
        self.cache[1] = data
        self.assertEqual(self.cache[1], data)
