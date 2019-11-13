"""
This module implements transposition tables, which store positions and moves to speed up tha algorithm
"""

import pickle



class TT:
    """
    Da creare nel game il seguente metodo
    game.ttentry() -> string or tuple

    che restituisce una tupla con variabile del gioco(mossa) in questo caso numpy array

    """

    def __init__(self, own_dict=None):
        self.d = own_dict if own_dict is not None else dict()

    def lookup(self, game):

        return self.d.get(game.ttentry(), None)

    def __call__(self, game):
        return self.d[game.ttentry()]['move']

    def store(self, **data):
        entry = data.pop("game").ttentry()
        self.d[entry] = data

    def tofile(self, filename):
        with open(filename, 'w+') as f:
            pickle.dump(self, f)

    def fromfile(self, filename):
        with open(filename, 'r') as h:
            self.__dict__.update(pickle.load(h).__dict__)


