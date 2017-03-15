from collections import OrderedDict


class NoDupOrderedDict(OrderedDict):
    """ Rejects duplicate definitions """
    
    def __init__(self, clsname):
        self.clsname = clsname
        super().__init__()
        
    def __setitem__(self, name, value):
        if name in self:
            raise TypeError('{} already defined in {}'.format(name, self.clsname))
        super().__setitem__(name, value)

