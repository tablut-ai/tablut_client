import sys, os, timeit, cProfile
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

def main():
    setup = "\
from random import randrange \n\
import numpy as np \n\
from game.game_numpy import GameNumpy \n\
from heuristic.eval_numpy import HeuristicNumpy \n\
from search.alphabeta import start_search \n\
game = GameNumpy() \n\
heuristic = HeuristicNumpy() \n\
state = np.array([ \n\
    [0, 0, 0, -1, -1, -1, 0, 0, 0], \n\
    [0, 0, 0, 0, -1, 0, 0, 0, 0], \n\
    [0, 0, 0, 0, 1, 0, 0, 0, 0], \n\
    [-1, 0, 0, 0, 1, 0, 0, 0,-1], \n\
    [-1, -1, 1, 1, 2, 1, 1, -1, -1], \n\
    [-1, 0, 0, 0, 1, 0, 0, 0, -1], \n\
    [0, 0, 0, 0, 1, 0, 0, 0, 0], \n\
    [0, 0, 0, 0, -1, 0, 0, 0, 0], \n\
    [0, 0, 0, -1, -1, -1, 0, 0, 0]]) \n\
heuristic.update(state) \n\
turn = 1 \n"

    search = "start_search(game, state, turn, heuristic)"

    print("====== Benchmark alphabeta search =====")
    print(avg_time(search, setup, 1))

    print("====== Profiler alphabeta search =====")
    cProfile.run(setup+search)

    print("====== All benchmark completed! =====")

def avg_time(stm, setup, n):
    return str(timeit.timeit(stm, setup=setup, number=n) / n * 1e6) + " us"

if __name__ == '__main__': main()