from collections import OrderedDict

class Cache:
    def __init__(self, size):
        self.od = OrderedDict()
        self.size = size

    def get(self, key, default=None):
        try: return self.od[key]
        except KeyError: return default

    def __setitem__(self, key, value):
        if len(self.od) > self.size:
            del self.od.keys()[0]
        self.od[key] = value

    def merge(self, that):
        self.od = {**self.od, **that.od}