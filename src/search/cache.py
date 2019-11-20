from collections import OrderedDict
from search.zobrist_hash import ZobristHash

class LRUCache:
    def __init__(self, size=1e8):
        self.od = OrderedDict()
        self.zhash = ZobristHash()
        self.size = size

    def get(self, state, default=None):
        key = self.zhash.compute(state)
        try: self.od.move_to_end(key)
        except KeyError: return default
        return self.od[key]

    def __setitem__(self, state, value):
        key = self.zhash.compute(state)
        try: del self.od[key]
        except KeyError:
            if len(self.od) == self.size:
                self.od.popitem(last=False)
        self.od[key] = value
