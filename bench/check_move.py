import timeit
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from game import TablutGame

def main():

    setup = "\
from random import randrange \n\
from game import TablutGame \n\
game = TablutGame() \n\
state = {'board': [ \n\
    ['O', 'O', 'O', 'B', 'B', 'B', 'O', 'O', 'O'], \n\
    ['O', 'O', 'O', 'O', 'B', 'O', 'O', 'O', 'O'], \n\
    ['O', 'O', 'O', 'O', 'W', 'O', 'O', 'O', 'O'], \n\
    ['B', 'O', 'O', 'O', 'W', 'O', 'O', 'O', 'B'], \n\
    ['B', 'B', 'W', 'W', 'K', 'W', 'W', 'B', 'B'], \n\
    ['B', 'O', 'O', 'O', 'W', 'B', 'O', 'O', 'B'], \n\
    ['O', 'O', 'O', 'O', 'W', 'O', 'O', 'O', 'O'], \n\
    ['O', 'O', 'O', 'O', 'B', 'O', 'O', 'O', 'O'], \n\
    ['O', 'O', 'O', 'B', 'B', 'B', 'O', 'O', 'O']  \n\
    ], 'turn': 'WHITE' \n\
}"

    check_move = 'game.check_move(state, {"from": [randrange(8), randrange(8)], "to": [randrange(8), randrange(8)]})'

    result = 'game.result(state, {"from": [randrange(8), randrange(8)], "to": [randrange(8), randrange(8)]})'

    print("====== Benchmark game.check_move =====")
    print(avg_time(check_move, setup, 100000))

    print("====== Benchmark game.result =====")
    print(avg_time(result, setup, 100000))

    print("====== All benchmark completed! =====")

def avg_time(stm, setup, n):
    return timeit.timeit(stm, setup=setup, number=n) / n * 1e6

if __name__ == '__main__': main()