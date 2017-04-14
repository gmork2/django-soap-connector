import keyword
import re

from django.db import models
from django.db.models.base import ModelBase


class ModelFactory(ModelBase):
    @classmethod
    def __prepare__(cls, name, bases, *, debug=False, synchronize=False):
        # Convert to valid class name
        to_var = lambda v: re.sub('\W|^(?=\d)','_', v)
        if name.isidentifier():
            name = to_var(name)
        name += ('', '_')[keyword.iskeyword(name)]

    def __init__(self, name, bases, ns, *, debug=False, synchronize=False):
        # Create cache for class instances
        super().__init__(name, bases, ns)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self, *args):
        if args in self.__cache:
            logger.info(self.__cache[args])
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
        return obj


