from unittest import skip
import time

from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from soap_connector.cache import *
from soap_connector.tests.api.utils import DummyView


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


class CacheIteratorTestCase(BaseTestCase):
    """

    """
    def setUp(self):
        """

        :return:
        """
        super().setUp()
        key = CacheIterator.pk_name

        self.data_list = [
            {key: 1, 'field': 'test_1'},
            {key: 2, 'field': 'test_2'},
            {key: 3, 'field': 'test_3'}
        ]

    def test_iterable(self):
        """

        :return:
        """
        it = CacheIterator(self.data_list, DummyView, self.context['view'])
        self.assertTrue(hasattr(it, '__iter__'))

    def test_simple(self):
        """

        :return:
        """
        it = CacheIterator(self.data_list, DummyView, self.context['view'])
        data_list = [i for i in it]

        self.assertListEqual(data_list, self.data_list)

    def test_iterate_empty_list(self):
        """

        :return:
        """
        it = CacheIterator([], DummyView, self.context['view'])
        data_list = [i for i in it]

        self.assertFalse(data_list)

    def test_invalid_data(self):
        """

        :return:
        """
        data_list = [{'id': 1, 'field': 'test_1'}]
        it = CacheIterator(data_list, DummyView, self.context['view'])

        self.assertRaises(
            KeyError, lambda: [i for i in it]
        )

    def test_cache_list(self):
        """

        :return:
        """
        view = self.context['view']
        it = CacheIterator(self.data_list, DummyView, view)
        pk_name = CacheIterator.pk_name

        _ = [i for i in it]

        with view.with_context(DummyView):
            for data in self.data_list:
                self.assertDictEqual(data, view.cache[data[pk_name]])


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
        object_class = self.context['view'].object_class
        key = self.registry.key

        self.assertIn(object_class.__name__, cache.get(key))

    def test_insert(self):
        """

        :return:
        """
        self.registry.insert(1)
        self.assertIn(1, self.registry.retrieve())
        self.registry.insert(2)
        self.assertEqual([1, 2], self.registry.retrieve())

    @skip("Not implemented")
    def test_insert_duplicate(self):
        """

        :return:
        """

    def test_retrieve_empty_registry(self):
        """

        :return:
        """
        self.assertEqual([], self.registry.retrieve())

    def test_remove(self):
        """

        :return:
        """
        self.registry.insert(1)
        self.registry.insert(2)
        self.registry.remove(1)
        self.assertEqual([2], self.registry.retrieve())

        self.registry.insert(3)
        self.registry.remove(3)
        self.assertEqual([2], self.registry.retrieve())

    def test_remove_empty_registry(self):
        """

        :return:
        """
        self.registry.remove(1)
        self.assertEqual([], self.registry.retrieve())

    def test_update(self):
        """

        :return:
        """
        values = [1, 2, 3]

        self.registry.update(values)
        self.assertEqual(values, self.registry.retrieve())

    def test_context(self):
        """

        :return:
        """
        url = reverse("soap_connector:root")
        request = APIRequestFactory().get(url)
        request.user = AnonymousUser()

        context = {
            'request': request,
            'view': DummyView(request=request)
        }
        registry = Registry(context=context)

        self.registry.insert(1)
        registry.insert(2)
        self.registry.insert(3)
        registry.insert(4)

        self.assertEqual([1, 3], self.registry.retrieve())
        self.assertEqual([2, 4], registry.retrieve())

    def test_expiration(self):
        """
        Cache values can be set to expire.

        :return:
        """
        self.registry.insert(1, 1)
        self.assertIn(1, self.registry.retrieve())
        time.sleep(2)
        self.assertEqual([], self.registry.retrieve())


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
        self.assertIsNotNone(self.cache.key)
        self.assertIsNotNone(self.cache.registry)

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
        Get in empty cache returns None.

        :return:
        """
        self.assertIsNone(self.cache[1])

    def test_delete(self):
        """

        :return:
        """
        self.cache[1] = self.data
        self.cache[2] = data = {
            'id': 2,
            'field': 'test_2'
        }
        del self.cache[1]

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
