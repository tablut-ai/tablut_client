import sys, os, timeit, cProfile, pstats
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

def main():
    setup = "\
from random import randrange \n\
import numpy as np \n\
from game.game_numpy import GameNumpy \n\
from game.game_obj import GameObj \n\
from heuristic.eval_numpy import HeuristicNumpy \n\
from heuristic.eval_obj import HeuristicObj \n\
from search.alphabeta import start_search \n\
game_np = GameNumpy() \n\
game_obj = GameObj() \n\
heuristic_np = HeuristicNumpy() \n\
heuristic_obj = HeuristicObj() \n\
state_np = np.array([ \n\
    [0, 0, 0, -1, -1, -1, 0, 0, 0], \n\
    [0, 0, 0, 0, -1, 0, 0, 0, 0], \n\
    [0, 0, 0, 0, 1, 0, 0, 0, 0], \n\
    [-1, 0, 0, 0, 1, 0, 0, 0,-1], \n\
    [-1, -1, 1, 1, 2, 1, 1, -1, -1], \n\
    [-1, 0, 0, 0, 1, 0, 0, 0, -1], \n\
    [0, 0, 0, 0, 1, 0, 0, 0, 0], \n\
    [0, 0, 0, 0, -1, 0, 0, 0, 0], \n\
    [0, 0, 0, -1, -1, -1, 0, 0, 0]]) \n\
state_obj = [ \n\
    [0, 0, 0, -1, -1, -1, 0, 0, 0], \n\
    [0, 0, 0, 0, -1, 0, 0, 0, 0], \n\
    [0, 0, 0, 0, 1, 0, 0, 0, 0], \n\
    [-1, 0, 0, 0, 1, 0, 0, 0,-1], \n\
    [-1, -1, 1, 1, 2, 1, 1, -1, -1], \n\
    [-1, 0, 0, 0, 1, 0, 0, 0, -1], \n\
    [0, 0, 0, 0, 1, 0, 0, 0, 0], \n\
    [0, 0, 0, 0, -1, 0, 0, 0, 0], \n\
    [0, 0, 0, -1, -1, -1, 0, 0, 0]] \n\
heuristic_np.update(state_np) \n\
heuristic_obj.update(state_obj) \n\
turn = 1 \n"

    search_np = "start_search(game_np, state_np, turn, heuristic_np)"

    search_obj = "start_search(game_obj, state_obj, turn, heuristic_obj)"

    #print("====== Benchmark alphabeta search numpy =====")
    #print(avg_time(search_np, setup, 1))

    #print("====== Benchmark alphabeta search python objects =====")
    #print(avg_time(search_obj, setup, 1))

    print("====== Profiler alphabeta search numpy =====")
    cProfile.run(setup+search_obj, sort="tottime", filename="/tmp/bench_alphabeta_search_obj.txt")
    p = pstats.Stats("/tmp/bench_alphabeta_search_obj.txt")
    p.sort_stats("tottime").print_stats(30)

    print("====== All benchmark completed! =====")

def avg_time(stm, setup, n):
    return str(timeit.timeit(stm, setup=setup, number=n) / n * 1e6) + " us"

if __name__ == '__main__': main()