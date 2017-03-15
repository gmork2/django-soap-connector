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

