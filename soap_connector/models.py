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

        def __new__(cls, name, bases, ns, *, debug=False, synchronize=False):
        """
        The constructor must register and cache all generated classes by
        itself. This behaviour prevents inconsistencies when class is
        redefined.
        """
        super_new = super().__new__

        # Follow the base class behavior when inherited explicitly
        # from models.Model
        parents = [b for b in bases if isinstance(b, models.Model)]
        if parents:
            return super_new(cls, name, bases, ns)
        
        # Context variables to determine the necessary fields and
        # relations with other classes
        _object = ns.pop('object')
        _parent = ns.get('parent', None)

        # Initialize registry for dynamic classes. If class has  
        # already been generated only create and store its instance from
        # context variables
        if not hasattr(cls, 'registry'):
            cls.registry = {}
        else:
            if name in cls.registry:
                instance = cls.create_instance(cls.registry[name], _object)
                cls.registry[name].queryset.append(instance)
                return cls.registry[name]
        
        # Create class with provided fields by _object. convert_to_fields
        # will add automatically a default manager
        ns.update(cls.convert_to_fields(_object, _parent))
        new_class = super_new(cls, name, (DeferredModel,), ns)

        # Remove queryset attribute if inherit from a generated class
        # by this constructor
        registers = tuple(new_class.registry.values())
        for base in bases:
            if isinstance(base, registers):
                del new_class.queryset

        # For each new class of model to establish a queryset containing a
        # number of instances obtained from successive calls to the factory
        # class with differents context variables. This queryset will be
        # used by the respective classes manager
        instance = cls.create_instance(new_class, _object, _parent)
        new_class.queryset = [instance]
        
        # Register new class
        cls.registry[name] = new_class
        
        return new_class



