import sys, os, timeit
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from game import TablutGame

def main():

    setup = "\
from native.state import cresult \n\
from random import randrange \n\
import numpy as np \n\
from game import TablutGame \n\
game = TablutGame() \n\
state = np.array([ \n\
    [0, 0, 0, -1, -1, -1, 0, 0, 0], \n\
    [0, 0, 0, 0, -1, 0, 0, 0, 0], \n\
    [0, 0, 0, 0, 1, 0, 0, 0, 0], \n\
    [-1, 0, 0, 0, 1, 0, 0, 0,-1], \n\
    [-1, -1, 1, 1, 2, 1, 1, -1, -1], \n\
    [-1, 0, 0, 0, 1, 0, 0, 0, -1], \n\
    [0, 0, 0, 0, 1, 0, 0, 0, 0], \n\
    [0, 0, 0, 0, -1, 0, 0, 0, 0], \n\
    [0, 0, 0, -1, -1, -1, 0, 0, 0]])"

    check_move = 'game.check_move(state, np.array([[randrange(8), randrange(8)], [randrange(8), randrange(8)]]), "WHITE")'

    result = 'game.result(state, np.array([[randrange(8), randrange(8)], [randrange(8), randrange(8)]]))'

    cresult = 'cresult(np.array([randrange(8), randrange(8), randrange(8), randrange(8)]))'

    print("====== Benchmark game.check_move =====")
    print(avg_time(check_move, setup, 200000))

    print("====== Benchmark game.result =====")
    print(avg_time(result, setup, 200000))

    print("====== Benchmark cython game.result =====")
    print(avg_time(cresult, setup, 200000))

    print("====== All benchmark completed! =====")

def avg_time(stm, setup, n):
    return timeit.timeit(stm, setup=setup, number=n) / n * 1e6

if __name__ == '__main__': main()