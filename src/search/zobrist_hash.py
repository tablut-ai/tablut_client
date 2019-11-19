import random

class ZobristHash:

    def __init__(self):
        self.table = [[[random.randint(1,2**64 - 1) for i in range(3)]for j in range(9)]for k in range(9)]

    def compute(self, board):
        h = 0
        for i in range(8):
            for j in range(8):
            # print board[i][j]
                if board[i][j] != '-':
                    piece = board[i][j]
                    h ^= self.table[i][j][piece]
        return h