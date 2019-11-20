import random

class ZobristHash:

    def __init__(self):
        self.table = [[[random.randint(1,2**64 - 1) for i in range(3)]for j in range(9)]for k in range(9)]

    def compute(self, board):
        h = 0
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    piece = board[i][j]
                    h ^= self.table[i][j][piece]
        return h