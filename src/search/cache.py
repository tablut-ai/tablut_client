
class LRUCache:
    def __init__(self, size=1e8):
        self.od = dict()
        self.size = size

    def get(self, key, default=None):
        try: return self.od[key]
        except KeyError: return default

    def __setitem__(self, key, value):
        self.od[key] = value

class HistoryHeuristic:
    def __init__(self, size=1e8):
        self.od = dict()
        self.size = size

    def get(self, move, default=None):
        key = (tuple(move[0]),tuple(move[1])) 
        try: return self.od[key]
        except KeyError: return default

    def __setitem__(self, move, depth):
        key = (tuple(move[0]),tuple(move[1])) 
        self.od[key] = depth
